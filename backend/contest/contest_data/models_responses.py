"""File with models description for response management."""

from contest_data.app import db
from datetime import datetime
import enum

APPEAL_MESSAGE_SIZE = 4000
FILETYPE_SIZE = 6


class Response(db.Model):
    """
    Class describing a Response model.

    work_id: id of the user's work
    user_id: id of the user
    contest_id: id of the contest
    """

    __tablename__ = 'response'

    work_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    contest_id = db.Column(db.Integer, nullable=False)  # TODO Add FK of contest, nullable until merge


class StatusEnum(enum.Enum):
    """
    Class enumerating statuses of user's work.

    not_checked: unchecked work
    accepted: accepted work
    rejected: rejected work
    appeal: work sent for appeal
    revision: work sent for revision
    appeal_accepted: appeal accepted
    appeal_rejected: appeal rejected
    """

    not_checked = 0
    accepted = 1
    rejected = 2
    appeal = 3
    revision = 4
    appeal_accepted = 5
    appeal_rejected = 6


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
    status = db.Column(db.Enum(StatusEnum), nullable=False)
    mark = db.Column(db.Integer)


class Appeal(db.Model):
    """
    Class describing a Appeal for the user's work.

    appeal_id: id of the user's appeal
    work_id: the work for which the appeal is submitted
    appeal_status: status of the appeal
    appeal_message: student's message for appeal
    appeal_response: expert's response for user's appeal
    """

    __tablename__ = 'appeal'

    appeal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    appeal_status = db.Column(db.Enum(StatusEnum), nullable=False)
    appeal_message = db.Column(db.String(APPEAL_MESSAGE_SIZE))
    appeal_response = db.Column(db.String(APPEAL_MESSAGE_SIZE))


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
    task_num = db.Column(db.Integer, nullable=False)  # TODO FK на заданий
    answer = db.Column(db.LargeBinary, nullable=False)
    filetype = db.Column(db.String(FILETYPE_SIZE), nullable=False)


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
