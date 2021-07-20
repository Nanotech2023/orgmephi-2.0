from backend.contest.app import db

from sqlalchemy import Identity, ForeignKey, CheckConstraint
from sqlalchemy.types import Boolean
from sqlalchemy.types import BLOB

# Constants

DEFAULT_VISIBILITY = False

# Contest models


class Composite_contest(db.Model):
    """
    Contest model
    """
    __tablename__ = 'composite_contest'

    contest_id = db.Column(db.Integer, ForeignKey('contest.contest_id'), Identity(start=0), primary_key=True)
    description = db.Column(db.Text, nullable=False)
    rules = db.Column(db.Text, nullable=False)
    # TODO task = db.Column(db.String(CONTEST_TASK_LINK))
    winning_condition = db.Column(db.Text, nullable=False)
    certificate_template = db.Column(db.Text, nullable=True)
    visibility = db.Column(Boolean(), default=DEFAULT_VISIBILITY, nullable=False)


class Contest_stage(db.Model):
    """
    Model "Contest stage"
    """
    __tablename__ = 'contest_stage'

    stage_id = db.Column(db.Integer, Identity(start=0), primary_key=True)
    stage_name = db.Column(db.Text)
    composite_contest_id = db.Column(db.Integer, ForeignKey('composite_contest.contest_id'), primary_key=True)
    next_stage_condition = db.Column(db.Text, nullable=False)


class Contests_in_Stage(db.Model):
    """
    Model "Contest in Composite stage"
    """
    __tablename__ = 'contests_in_stage'

    stage_id = db.Column(db.Integer, ForeignKey('contest_stage.contest_id'), primary_key=True)
    contest_id = db.Column(db.Integer, ForeignKey('composite_contest.contest_id'), primary_key=True)


class Contests_in_Composite_contest(db.Model):
    """
    Model "Contest in Composite stage"
    """
    __tablename__ = 'contests_in_composite_contest'

    composite_contest_id = db.Column(db.Integer, ForeignKey('composite_contest.contest_id'), primary_key=True)
    contest_id = db.Column(db.Integer, ForeignKey('composite_contest.contest_id'), primary_key=True)


# Tasks models

class Task_variant(db.Model):
    """
    Model "Variant of the task"
    """

    __tablename__ = 'task_variant'

    variant_id = db.Column(db.Integer, Identity(start=0), primary_key=True)
    variant_number = db.Column(db.Integer)
    variant_description = db.Column(db.Text)


class Task_in_variant(db.Model):
    """
    Model "Task in variant"

    :param task_type: "Plain", "Range", "Multiply"
    """
    __tablename__ = 'task_in_variant'

    variant_id = db.Column(db.Integer, ForeignKey('task_variant.variant_id'), primary_key=True)
    task_type = db.Column(db.String, nullable=False)
    task_id = db.Column(db.Integer, primary_key=True)

    __table_args__ = (
        CheckConstraint(task_type in ["Plain", "Range", "Multiply"], name='check_bar_positive'),
        {})


class Plain_Task(db.Model):
    """
    Model "Task with Plain Text"
    """
    __tablename__ = 'plain_task'

    task_id = db.Column(db.Integer, Identity(start=0), primary_key=True)
    num_of_task = db.Column(db.Integer, nullable=False)
    image_of_task = db.Column(BLOB, nullable=False)
    recommended_answer = db.Column(db.Text, nullable=False)


class Range_Task(db.Model):
    """
    Model "Task with Range"
    """
    __tablename__ = 'range_task'

    task_id = db.Column(db.Integer, Identity(start=0), primary_key=True)
    num_of_task = db.Column(db.Integer, nullable=False)
    image_of_task = db.Column(BLOB, nullable=False)
    start_value = db.Column(db.Text, nullable=False)
    end_value = db.Column(db.Text, nullable=False)


class Multiply_Task(db.Model):
    """
    Model "Task with multiply choice"
    """
    __tablename__ = 'multiply_task'

    task_id = db.Column(db.Integer, Identity(start=0), primary_key=True)
    num_of_task = db.Column(db.Integer, nullable=False)
    image_of_task = db.Column(BLOB, nullable=False)
    recommended_answer = db.Column(db.Text, nullable=False)


class Answers_in_Multiply_Task(db.Model):
    """
    Model "Task with multiply choice"
    """
    __tablename__ = 'answers_in_multiply_task'

    task_id = db.Column(db.Integer, ForeignKey('multiply_task.task_id'), primary_key=True)
    suggested_answer = db.Column(db.Integer, primary_key=True)



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
