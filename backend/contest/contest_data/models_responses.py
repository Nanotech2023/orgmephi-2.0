"""File with models description for response management."""

from app import db
from sqlalchemy import Identity, BLOB, CheckConstraint
from datetime import datetime

RESPONSE_STATUS_SIZE = 15
APPEAL_MESSAGE_SIZE = 4000
RESPONSE_ANSWER_SIZE = 250  # TODO узнать у Миши.
IDENTITY_START = 0
DEFAULT_MARK_VALUE = 0


class Response(db.Model):
    """
    Class describing a Response model.

    work_id: id of the user's work
    user_id: id of the user
    contest_id: id of the contest
    """

    __tablename__ = 'response'

    work_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    user_id = db.Column(db.Integer)
    contest_id = db.Column(db.Integer)  # TODO Add FK of contest


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

    status_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.Integer, db.ForeignKey('statusofwork.status_id'))
    mark = db.Column(db.Integer, default=DEFAULT_MARK_VALUE)

    __table_args__ = (
        CheckConstraint('0 <= mark <= 100', name='check_mark_0_100'),
        {})


class Status(db.Model):
    """
    Class describing a Status model.

    status_id: id of the status
    status: word description of the status - not_checked/checked/rejected/appeal/revision
    """

    __tablename__ = 'statusofwork'

    status_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    status = db.Column(db.String(RESPONSE_STATUS_SIZE), unique=True)


class Appeal(db.Model):
    """
    Class describing a Appeal for the user's work.

    appeal_id: id of the user's appeal
    work_id: the work for which the appeal is submitted
    appeal_message: student's message for appeal
    appeal_response: expert's response for user's appeal
    """

    __tablename__ = 'appeal'

    appeal_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    appeal_message = db.Column(db.String(APPEAL_MESSAGE_SIZE))
    appeal_response = db.Column(db.String(APPEAL_MESSAGE_SIZE))


class ResponseAnswer(db.Model):
    """
    Class describing user's answers in response.

    answer_id: id of the user's answer
    work_id: id of the user's work
    task_num: id of the task
    answer: user's answer
    """

    __tablename__ = 'responseanswer'

    answer_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    task_num = db.Column(db.Integer)  # TODO FK на заданий
    answer = db.Column(db.String)


class ResponseFile(db.Model):
    """
    Class describing user's file in response.

    file_id: id of the file
    work_id: id of the user's work
    file: user's file
    """

    __tablename__ = 'responsefile'

    file_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))  # TODO привязка к заданию или к работе
    file = db.Column(BLOB)


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
