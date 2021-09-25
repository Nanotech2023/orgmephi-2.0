"""File with models description for response management."""

from datetime import datetime, timedelta
import enum
from sqlalchemy.ext.associationproxy import association_proxy
from common import get_current_db
from contest.tasks.models import UserInContest, Task, MultipleChoiceTask, PlainTask, RangeTask
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
        contest_id=contest_id
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
    work_status = db.Column(db.Enum(ResponseStatusEnum), default=ResponseStatusEnum.in_progress, nullable=False)

    answers = db.relationship('BaseAnswer', backref='response', lazy='dynamic', cascade="all, delete")

    @hybrid_property
    def mark(self):
        mark = 0
        for elem in self.answers:
            mark += elem.mark
        return mark

    @hybrid_property
    def status(self):
        from common.util import db_get_one_or_none
        from messages.models import Thread, ThreadStatus, ThreadType
        thread = db_get_one_or_none(Thread, 'related_work_id', self.work_id)
        if thread is not None:
            if thread.status == ThreadStatus.open and thread.thread_type == ThreadType.appeal:
                return work_status['Appeal']
            else:
                return self.work_status
        else:
            return self.work_status


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
    PlainAnswerText = "PlainAnswerText"
    PlainAnswerFile = "PlainAnswerFile"
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
    task_id = db.Column(db.Integer, db.ForeignKey(Task.task_id))
    answer_type = db.Column(db.Enum(AnswerEnum), nullable=False)
    mark = db.Column(db.Float, default=0)

    task = db.relationship(Task, uselist=False)
    task_points = association_proxy('task', 'task_points')

    __mapper_args__ = {
        'polymorphic_identity': AnswerEnum.BaseAnswer,
        'polymorphic_on': answer_type
    }

    @hybrid_property
    def right_answer(self):
        from common.util import db_get_one_or_none
        if self.answer_type.value == "PlainAnswerText" or self.answer_type.value == "PlainAnswerFile":
            task: PlainTask = db_get_one_or_none(PlainTask, 'task_id', self.task_id)
            if task.show_answer_after_contest:
                return {'answer': task.recommended_answer}
        elif self.answer_type.value == "RangeAnswer":
            task: RangeTask = db_get_one_or_none(RangeTask, 'task_id', self.task_id)
            if task.show_answer_after_contest:
                return {
                    'start_value': task.start_value,
                    'end_value': task.end_value,
                }
        elif self.answer_type.value == "MultipleChoiceAnswer":
            task: MultipleChoiceTask = db_get_one_or_none(MultipleChoiceTask, 'task_id', self.task_id)
            right_answers = [elem['answer'] for elem in task.answers if elem['is_right_answer']]
            if task.show_answer_after_contest:
                return {'answers': right_answers}


def add_range_answer(work_id, task_id, values):
    answer = RangeAnswer(
        work_id=work_id,
        task_id=task_id,
        answer=values['answer']
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
        'with_polymorphic': '*'
    }


def add_plain_answer_text(work_id, task_id, values):
    answer = PlainAnswerText(
        work_id=work_id,
        task_id=task_id,
        answer_text=values['answer_text']
    )
    db.session.add(answer)


class PlainAnswerText(BaseAnswer):
    """
    Class describing answer for plain task with text

    answer_id: id of the answer
    answer_text: user's answer
    """

    answer_id = db.Column(db.Integer, db.ForeignKey(BaseAnswer.answer_id), primary_key=True)
    answer_text = db.Column(db.Text)

    __mapper_args__ = {
        'polymorphic_identity': AnswerEnum.PlainAnswerText,
        'with_polymorphic': '*'
    }


def add_plain_answer_file(work_id, task_id, filetype, file):
    answer = PlainAnswerFile(
        work_id=work_id,
        task_id=task_id,
        answer_file=file,
        filetype=filetype
    )
    db.session.add(answer)


class PlainAnswerFile(BaseAnswer):
    """
    Class describing answer for plain task

    answer_id: id of the answer
    answer_file: user's answer as a file
    filetype: user's answer filetype
    """

    answer_id = db.Column(db.Integer, db.ForeignKey(BaseAnswer.answer_id), primary_key=True)
    answer_file = db.Column(db.LargeBinary)
    filetype = db.Column(db.Enum(ResponseFiletypeEnum))

    __mapper_args__ = {
        'polymorphic_identity': AnswerEnum.PlainAnswerFile,
        'with_polymorphic': '*'
    }

    def update(self, answer_new=None, filetype_new=None):
        if answer_new is not None:
            self.answer_file = answer_new
        if filetype_new is not None:
            self.filetype = filetype_dict[filetype_new]


def add_multiple_answer(work_id, task_id, values):
    answer = MultipleChoiceAnswer(
        work_id=work_id,
        task_id=task_id,
        answers=set(elem['answer'] for elem in values['answers'])
    )
    db.session.add(answer)


class MultipleChoiceAnswer(BaseAnswer):
    """
    Class describing answer for multiple choice answer

    answer_id: id of the answer
    answers: answers
    """

    answer_id = db.Column(db.Integer, db.ForeignKey(BaseAnswer.answer_id), primary_key=True)

    answers = db.Column(db.PickleType)

    __mapper_args__ = {
        'polymorphic_identity': AnswerEnum.MultipleChoiceAnswer,
        'with_polymorphic': '*'
    }
