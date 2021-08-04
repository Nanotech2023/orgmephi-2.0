"""File with models description for response management."""

from contest_data import db
from datetime import datetime
import enum


class Response(db.Model):
    """
    Class describing a Response model.

    work_id: id of the user's work
    user_id: id of the user
    contest_id: id of the contest
    """

    __tablename__ = 'response'

    work_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_in_contest.user_id'))
    contest_id = db.Column(db.Integer, db.ForeignKey('user_in_contest.contest_id'))
    statuses = db.relationship('responsestatus', backref='response', lazy=True)
    answers = db.relationship('responseanswer', backref='response', lazy=True)


class ResponseStatusEnum(enum.Enum):
    """
    Class enumerating statuses of user's work.

    not_checked: unchecked work
    accepted: accepted work
    rejected: rejected work
    appeal: work sent for appeal
    revision: work sent for revision
    """

    not_checked = 'NotChecked'
    accepted = 'Accepted'
    rejected = 'Rejected'
    appeal = 'Appeal'
    revision = 'Revision'


work_status = {status.value: status for status in ResponseStatusEnum}
work_status_reverse = {val: key for key, val in work_status.items()}


class ResponseStatus(db.Model):
    """
    Class describing a Response Status model.

    status_id: id of the status
    work_id: id of the user's work
    timestamp: timestamp to determine the timeline
    status: status of the work
    mark: mark of the work
    """

    __tablename__ = 'responsestatus'

    status_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.Enum(ResponseStatusEnum), nullable=False)
    mark = db.Column(db.Float)

    def serialize(self):
        if self.mark is None:
            return {
                'status':work_status_reverse[self.status]
            }
        else:
            return {
                'status': work_status_reverse[self.status],
                'mark': self.mark
            }


class AppealStatusEnum(enum.Enum):
    """
    Class enumerating statuses of user's work appeal.

    under_review: appeal has been submitted and is under review
    appeal_accepted: appeal accepted
    appeal_rejected: appeal rejected
    """

    under_review = "UnderReview"
    appeal_accepted = "AppealAccepted"
    appeal_rejected = "AppealRejected"


appeal_status = {status.value: status for status in AppealStatusEnum}
appeal_status_reverse = {val: key for key, val in appeal_status.items()}


class Appeal(db.Model):
    """
    Class describing a Appeal for the user's work.

    appeal_id: id of the user's appeal
    work_status: the status of the work on which the appeal was submitted
    appeal_status: status of the appeal
    appeal_message: student's message for appeal
    appeal_response: expert's response for user's appeal
    """

    __tablename__ = 'appeal'

    appeal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    work_status = db.Column(db.Integer, db.ForeignKey('responsestatus.status_id'))
    appeal_status = db.Column(db.Enum(AppealStatusEnum), nullable=False)
    appeal_message = db.Column(db.Text)
    appeal_response = db.Column(db.Text)

    def serialize(self):
        return {
                'appeal_id': self.appeal_id,
                'status': self.work_status,
                'appeal_message': self.appeal_message,
                'appeal_response': self.appeal_response
            }

    def reply_to_appeal(self, message, status):
        self.appeal_response = message
        self.appeal_status = status


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
filetype_reverse = {val: key for key, val in filetype_dict.items()}


class ResponseAnswer(db.Model):
    """
    Class describing user's answers in response.

    answer_id: id of the user's answer
    work_id: id of the user's work
    task_num: id of the task
    answer: user's answer as a file
    filetype: user's answer filetype
    """

    __tablename__ = 'responseanswer'

    answer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    task_num = db.Column(db.Integer, db.ForeignKey('base_task.task_id'))
    answer = db.Column(db.LargeBinary, nullable=False)
    filetype = db.Column(db.Enum(ResponseFiletypeEnum), nullable=False)

    def serialize(self):
        return {
            'task_id': self.task_num,
            'answer_id': self.answer_id
        }

    def update(self, answer_new=None, filetype_new=None):
        if answer_new is not None:
            self.answer = answer_new
        if filetype_new is not None:
            self.filetype = filetype_dict[filetype_new]


def get_one_or_null(entity, field, value):
    return entity.query.filter_by(**{field: value}).one_or_none()


def get_list(entity, field, value):
    return entity.query.filter_by(**{field: value}).all()


def add_user_response(db_session, user_id, contest_id):
    user_work = Response(
        user_id=user_id,
        contest_id=contest_id
    )
    db_session.add(user_work)
    db_session.flush()
    return user_work


def add_response_status(db_session, work_id, status=None, mark=None):
    if status is None:
        new_status = work_status['NotChecked']
    else:
        new_status = work_status[status]
    if mark is None:
        response_status = ResponseStatus(
            work_id=work_id,
            status=new_status
        )
    else:
        response_status = ResponseStatus(
            work_id=work_id,
            status=new_status,
            mark=mark
        )
    db_session.add(response_status)
    db_session.flush()
    return response_status


def add_response_answer(db_session, work_id, task_id, answer, filetype):
    response_answer = ResponseAnswer(
        work_id=work_id,
        task_num=task_id,
        answer=answer,
        filetype=filetype_dict[filetype]
    )
    db_session.add(response_answer)
    db_session.flush()
    return response_answer


def get_status_history(db_session, work_id, status):
    history = []
    appeals = ResponseStatus.query.join(Appeal, ResponseStatus.status_id == Appeal.work_status). \
        filter_by(ResponseStatus.work_id == work_id). \
        order_by(ResponseStatus.timestamp.desc()).all()
    number = 0
    if appeals is None:
        appeals = []
    for elem in status:
        if len(appeals) > number and appeals[number].work_status == elem.status_id:
            appeal = appeals.appeal_id
            number += 1
        else:
            appeal = None
        history.append(
            {
                'status:': work_status_reverse[elem.status],
                'datetime': elem.timestamp,
                'appeal_id': appeal,
                'mark': elem.mark
            }
        )


def add_response_appeal(db_session, status_id, message):
    appeal = Appeal(
        work_status=status_id,
        appeal_status=appeal_status['UnderReview'],
        appeal_message=message
    )
    db_session.add(appeal)
    db_session.flush()
    return response_answer


if __name__ == '__main__':
    db.create_all()
