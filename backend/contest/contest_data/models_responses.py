from backend.contest.app import db
from sqlalchemy import Identity, ForeignKey
from datetime import datetime

RESPONSE_STATUS_SIZE = 15
IDENTITY_START = 0


class Response(db.Model):
    __tablename__ = 'response'

    work_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(''))  # TODO Add FK of user
    contest_id = db.Column(db.Integer, db.ForeignKey(''))  # TODO Add FK of contest


class ResponseStatus(db.Model):
    __tablename__ = 'responsestatus'

    status_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.String(RESPONSE_STATUS_SIZE))
    """not_checked/checked/rejected/appeal/revision"""
    mark = db.Column(db.Integer)


class Appeal(db.Model):
    __tablename__ = 'appeal'

    appeal_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    inspector_id = db.Column(db.Integer, db.ForeignKey(''))  # TODO Add FK of inspector


class AppealMessage(db.Model):
    __tablename__ = 'appealmessage'

    message_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    appeal_id = db.Column(db.Integer, db.ForeignKey('appeal.appeal_id'))
    user_id = db.Column(db.Integer, db.ForeignKey(''))  # TODO Add FK of user
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    message = db.Column(db.Text)  # TODO сколько выделять для сообшения или хранить файлом?


class ResponseAnswer(db.Model):
    __tablename__ = 'responseanswer'

    answer_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    task_num = db.Column(db.Integer)
    answer = db.Column(db.Text)


class ResponseFile(db.Model):
    __tablename__ = 'responsefile'

    file_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    filename = db.Column(db.Text)


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
