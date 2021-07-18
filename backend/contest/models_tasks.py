from backend.contest.app import db

from sqlalchemy import Identity, ForeignKey
from sqlalchemy.types import Boolean, BIGINT

# Constants

CONTEST_DESCRIPTION_SIZE = 200
CONTEST_RULES_SIZE = 200
CONTEST_WINNING_CONDITION_SIZE = 200
NEXT_STAGE_CONDITION_SIZE = 200
DEFAULT_VISIBILITY = False
CONTEST_TEMPLATE_LINK = 200

# TODO
# Что является заданием? Ссылка куда-то?
CONTEST_TASK_LINK = 200


class Contest(db.Model):
    __tablename__ = 'contest'

    contest_id = db.Column(BIGINT(), Identity(start=0), primary_key=True)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'contest',
        'polymorphic_on': type
    }


class Simple_contest(db.Model):
    __tablename__ = 'simple_contest'

    contest_id = db.Column(BIGINT(), ForeignKey('contest.contest_id'), Identity(start=0), primary_key=True)
    description = db.Column(db.String(CONTEST_DESCRIPTION_SIZE))
    rules = db.Column(db.String(CONTEST_RULES_SIZE))
    task = db.Column(db.String(CONTEST_TASK_LINK))
    winning_condition = db.Column(db.String(CONTEST_WINNING_CONDITION_SIZE))
    certificate_template = db.Column(db.String(CONTEST_TEMPLATE_LINK))
    visibility = db.Column(Boolean(), default=DEFAULT_VISIBILITY)

    __mapper_args__ = {
        'polymorphic_identity': 'simple_contest'
    }


class Composite_contest(db.Model):
    __tablename__ = 'composite_contest'

    contest_id = db.Column(BIGINT(), ForeignKey('contest.contest_id'), Identity(start=0), primary_key=True)
    description = db.Column(db.String(CONTEST_DESCRIPTION_SIZE))
    visibility = db.Column(Boolean(), default=DEFAULT_VISIBILITY)

    __mapper_args__ = {
        'polymorphic_identity': 'composite_contest'
    }


class Contest_stage(db.Model):
    __tablename__ = 'stage'

    stage_id = db.Column(BIGINT(), Identity(start=0), primary_key=True)
    contest_id = db.Column(BIGINT(), ForeignKey('composite_contest.contest_id'), primary_key=True)
    next_stage_condition = db.Column(db.String(NEXT_STAGE_CONDITION_SIZE))


class Contests_in_stage(db.Model):
    __tablename__ = 'contests_in_stage'

    stage_id = db.Column(BIGINT(), ForeignKey('stage.stage_id'), primary_key=True)
    parent_contest_id = db.Column(BIGINT(), ForeignKey('stage.contest_id'), primary_key=True)
    contest_id = db.Column(BIGINT(), ForeignKey('contest.contest_id'), primary_key=True)


"""
Возможные запросы:
- Создавать, редактировать, удалять и предоставлять доступ к карточке конкурса; 
- Создавать, редактировать, удалять и предоставлять доступ к карточке этапа;
- Добавлять и удалять этапы в структуре конкурса;
- Генерацию документа для печати сертификатов.


- Редактирование описания и метаинформацию конкурсов и этапов
- Редактировать структуру конкурсного мероприятия, добавлять и удалять этапы, изменять видимость конкурса
- Загружать шаблоны и отправлять на печатать дипломы и сертификаты. 

"""
