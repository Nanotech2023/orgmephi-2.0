"""File with models description for response management."""

from datetime import datetime
import enum
from common import get_current_db

db = get_current_db()


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
    statuses = db.relationship('ResponseStatus', backref='response', lazy=True)
    answers = db.relationship('ResponseAnswer', backref='response', lazy=True)


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


"""
Возможные запросы:
    - Получение ведомости пользователей для определенного конкурса - пользователь/ оценка
    - Отображение переписки между проряющим и пользователем во время аппеляции
    - Отобразить историю статусов для работы с оценками
    - Внести / Изменить ответ пользователя
    - Загрузить файл от пользователя
    - Выдать все ответы пользователя + файлы
    - Изменить статус работы
"""

if __name__ == '__main__':
    db.create_all()
