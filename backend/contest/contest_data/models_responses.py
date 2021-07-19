from backend.contest.app import db
from sqlalchemy import Identity, BLOB, CheckConstraint
from datetime import datetime

RESPONSE_STATUS_SIZE = 15
APPEAL_MESSAGE_SIZE = 4000
RESPONSE_ANSWER_SIZE = 250  # TODO узнать у Миши.
IDENTITY_START = 0


class Response(db.Model):
    __tablename__ = 'response'
    
    work_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    user_id = db.Column(db.Integer)
    contest_id = db.Column(db.Integer)  # TODO Add FK of contest


class ResponseStatus(db.Model):
    __tablename__ = 'responsestatus'

    status_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.Integer, db.ForeignKey('statusofwork.status_id'))
    mark = db.Column(db.Integer)

    __table_args__ = (
        CheckConstraint(0 <= mark <= 100, name='check_mark_0_100'),
        {})


class Status(db.Model):
    __tablename__ = 'statusofwork'

    status_id = db.Column(db.Integer)
    status = db.Column(db.String(RESPONSE_STATUS_SIZE), unique=True)


class Appeal(db.Model):
    __tablename__ = 'appeal'

    appeal_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    appeal_message = db.Column(db.String(APPEAL_MESSAGE_SIZE))
    appeal_response = db.Column(db.String(APPEAL_MESSAGE_SIZE))


class ResponseAnswer(db.Model):
    __tablename__ = 'responseanswer'

    answer_id = db.Column(db.Integer, Identity(start=IDENTITY_START), primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('response.work_id'))
    task_num = db.Column(db.Integer)  # TODO FK на заданий
    answer = db.Column(db.String)


class ResponseFile(db.Model):
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
