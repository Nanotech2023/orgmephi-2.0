"""File with models description for response management."""

from datetime import datetime, timedelta
import enum
from common import get_current_db
from contest.tasks.models import UserInContest, Task
from messages.models import Thread
from common.util import db_get_one_or_none
from sqlalchemy.ext.hybrid import hybrid_property

db = get_current_db()


class ResponseStatusEnum(enum.Enum):
    """
    Class enumerating statuses of user's work.

    not_checked: unchecked work
    accepted: accepted work
    rejected: rejected work
    appeal: work sent for appeal
    correction: work sent for correction
    """

    in_progress = 'InProgress'
    not_checked = 'NotChecked'
    accepted = 'Accepted'
    rejected = 'Rejected'
    appeal = 'Appeal'
    correction = 'Correction'


work_status = {status.value: status for status in ResponseStatusEnum}


def add_user_response(db_session, user_id, contest_id):
    user_work = Response(
        user_id=user_id,
        contest_id=contest_id,
        status=work_status['InProgress']
    )
    db_session.add(user_work)
    return user_work


class Response(db.Model):
    """
    Class describing a Response model.

    work_id: id of the user's work
    user_id: id of the user
    contest_id: id of the contest
    start_time: start time of the olympiad
    finish_time: finish time of the olympiad
    status: status of the response

    appeal: appeal to user response
    answers: answers in user response
    """

    work_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(UserInContest.user_id))
    contest_id = db.Column(db.Integer, db.ForeignKey(UserInContest.contest_id))
    start_time = db.Column(db.DateTime, default=datetime.utcnow())
    finish_time = db.Column(db.DateTime, default=datetime.utcnow())
    time_extension = db.Column(db.Interval, default=timedelta(seconds=0))
    status = db.Column(db.Enum(ResponseStatusEnum), nullable=False)

    answers = db.relationship('BaseAnswer', backref='response', lazy='dynamic', cascade="all, delete")

    @hybrid_property
    def mark(self):
        mark = 0
        if len(self.answers) > 0:
            for elem in self.answers:
                mark += elem.mark
            return mark

    @hybrid_property
    def status(self):
        if db_get_one_or_none(Thread, 'related_work_id', self.work_id) is not None:
            return work_status['Appeal']
        else:
            return self.status

    @status.setter
    def status(self, value):
        self.status = value


class ResponseFiletypeEnum(enum.Enum):
    """
    Class enumerating all possible answer filetypes.

    txt: text document
    pdf: pdf file
    jpg: jpg picture
    doc: Microsoft Word format
    docx: new Microsoft Word format
    png: png picture
    gif: gif picture
    odt: OpenOffice format
    """

    txt = 'txt'
    pdf = 'pdf'
    jpg = 'jpg'
    doc = 'doc'
    docx = 'docx'
    png = 'png'
    gif = 'gif'
    odt = 'odt'


filetype_dict = {filetype.value: filetype for filetype in ResponseFiletypeEnum}


class AnswerEnum(enum.Enum):
    PlainAnswer = "PlainAnswer"
    RangeAnswer = "RangeAnswer"
    MultipleChoiceAnswer = "MultipleChoiceAnswer"
    BaseAnswer = "BaseAnswer"


answer_dict = {answer.value: answer for answer in AnswerEnum}


class BaseAnswer(db.Model):
    """
    Base class for user's answer

    answer_id: id of the user's answer
    work_id: id of the user's work
    task_id: id of the task
    """

    answer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    task_id = db.Column(db.Integer, db.ForeignKey(f'{Task.__tablename__}.task_id'))
    answer_type = db.Column(db.Enum(AnswerEnum), nullable=False)
    mark = db.Column(db.Float, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': AnswerEnum.PlainAnswer,
        'polymorphic_on': answer_type
    }


def add_range_answer(work_id, task_id, answer):
    answer = RangeAnswer(
        work_id=work_id,
        task_id=task_id,
        answer=answer
    )
    db.session.add(answer)


class RangeAnswer(BaseAnswer):
    """
    Class describing answer for range task

    answer_id: id of the answer
    answer: user answer
    """

    answer_id = db.Column(db.Integer, db.ForeignKey(BaseAnswer.answer_id), primary_key=True)
    answer = db.Column(db.Float, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': AnswerEnum.RangeAnswer,
    }


def add_plain_answer(work_id, task_id, text=None, filetype=None, file=None):
    if text is not None:
        answer = PlainAnswer(
            work_id=work_id,
            task_id=task_id,
            answer_text=text
        )
    else:
        answer = PlainAnswer(
            work_id=work_id,
            task_id=task_id,
            answer_file=file,
            filetype=filetype
        )
    db.session.add(answer)


class PlainAnswer(BaseAnswer):
    """
    Class describing answer for plain task

    answer_id: id of the answer
    answer: user's answer as a file
    filetype: user's answer filetype
    """

    answer_id = db.Column(db.Integer, db.ForeignKey(BaseAnswer.answer_id), primary_key=True)
    answer_text = db.Column(db.Text, nullable=True)
    answer_file = db.Column(db.LargeBinary, nullable=True)
    filetype = db.Column(db.Enum(ResponseFiletypeEnum), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': AnswerEnum.PlainAnswer,
    }

    def update(self, answer_new=None, filetype_new=None):
        if answer_new is not None:
            self.answer_file = answer_new
        if filetype_new is not None:
            self.filetype = filetype_dict[filetype_new]


def add_multiple_answer(work_id, task_id, answers):
    answer = MultipleUserAnswer(
        work_id=work_id,
        task_id=task_id
    )
    db.session.add(answer)
    for elem in answers:
        answer.answers.append(MultipleUserAnswer(text=elem))


class MultipleChoiceAnswer(BaseAnswer):
    """
    Class describing answer for multiple choice answer

    answer_id: id of the answer
    """

    answer_id = db.Column(db.Integer, db.ForeignKey(BaseAnswer.answer_id), primary_key=True)

    answers = db.relationship('MultipleUserAnswer', lazy='dynamic', cascade="all, delete")

    __mapper_args__ = {
        'polymorphic_identity': AnswerEnum.MultipleChoiceAnswer,
    }


class MultipleUserAnswer(db.Model):
    """
    Class describing each user answer for multiple choice task
    """

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey(MultipleChoiceAnswer.answer_id))
    answer = db.Column(db.Text, nullable=False)


if __name__ == '__main__':
    db.create_all()
