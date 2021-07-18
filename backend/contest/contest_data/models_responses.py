from app import db
from flask_sqlalchemy.dialects.postgresql import BIGINT
from datetime import datetime


class Response(db.Model):
    work_id = db.Column(BIGINT(unsigned=True),  Identity(start=0), primary_key=True)
    user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey()) #TODO Add FK of user
    contest_id = db.Column(BIGINT(unsigned=True), db.ForeignKey()) #TODO Add FK of contest

class ResponseStatus(db.Model):
    status_id = db.Column(BIGINT(unsigned=True), Identity(start=0), primary_key=True)
    work_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('response.work_id'))
    timestamp = db.Column(db.DateTime, index=True, default = datetime.utcnow)
    status = db.Column(db.String(15))
    """not_checked/checked/rejected/appeal/revision"""
    mark = db.Column(db.Integer)

class Appeal(db.Model):
    appeal_id = db.Column(BIGINT(unsigned=True), Identity(start=0), primary_key=True)
    work_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('response.work_id'))
    timestamp = db.Column(db.DateTime, index=True, default = datetime.utcnow)
    inspector_id = db.Column(BIGINT(unsigned=True), db.ForeignKey()) #TODO Add FK of inspector

class AppealMessages(db.Model):
    message_id = db.Column(BIGINT(unsigned=True), Identity(start=0), primary_key=True)
    appeal_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('appeal.appeal_id'))
    user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey()) #TODO Add FK of user
    timestamp = db.Column(db.DateTime, index=True, default = datetime.utcnow)
    message = db.Column(db.String()) #TODO сколько выделять для сообшения или хранить файлом?

class Answer(db.Model):
    answer_id = db.Column(BIGINT(unsigned=True), Identity(start=0), primary_key=True)
    work_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('response.work_id'))
    task_num = db.Column(db.Integer)
    answer = db.Column(db.String()) #TODO сколько выделять для ответа

class File(db.Model):
    file_id = db.Column(BIGINT(unsigned=True), Identity(start=0), primary_key=True)
    work_id = db.Column(BIGINT(unsigned=True), db.ForeignKey('response.work_id'))
    filename = db.Column(db.String(250))

'''
Возможные запросы:
    - Получение ведости пользователей для определенного конкурса - пользователь/ оценка
    - Отображение переписки между проряющим и пользователем во время аппеляции
    - Отобразить историю статусов для работы с оценками
    - Изменить ответ пользователя
    - Внести ответ пользователя
    - Загрузить файл от пользователя
    - Выдать все ответы пользователя + файлы
'''

"""
Вопросы:
    - 
"""