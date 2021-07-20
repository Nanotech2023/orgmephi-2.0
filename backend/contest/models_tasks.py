"""File with models description for contests and tasks management."""
from app import db

# Constants

DEFAULT_VISIBILITY = False


# Contest models


class CompositeContest(db.Model):
    """
    Class describing a Composite contest model.

    contest_id: id of contest
    description: description of the contest
    rules: rules of the contest
    variant_id: variant connected with current contest
    winning_condition: winning condition
    certificate_template: contest certificate template
    visibility: visibility of the contest
    """

    __tablename__ = 'composite_contest'

    contest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    rules = db.Column(db.Text, nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('task_variant.variant_id'))
    winning_condition = db.Column(db.Text, nullable=False)
    certificate_template = db.Column(db.Text, nullable=True)
    visibility = db.Column(db.Boolean, default=DEFAULT_VISIBILITY, nullable=False)
    __table_args__ = {'extend_existing': True}


class ContestStage(db.Model):
    """
    Class describing a Stage model.

    stage_id: id of the stage
    stage_name: name of the stage
    composite_contest_id: if of the composite contest
    next_stage_condition: condition to pass to the next stage
    """

    __tablename__ = 'contest_stage'

    stage_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    stage_name = db.Column(db.String(50), index=True)
    composite_contest_id = db.Column(db.Integer, db.ForeignKey('composite_contest.contest_id'), primary_key=True)
    next_stage_condition = db.Column(db.Text, nullable=False)
    __table_args__ = {'extend_existing': True}


class ContestsInStage(db.Model):
    """
    Class describing a Contests In Stage model.

    ///
    """

    __tablename__ = 'contests_in_stage'

    stage_id = db.Column(db.Integer, db.ForeignKey('contest_stage.stage_id'), primary_key=True)
    contest_id = db.Column(db.Integer, db.ForeignKey('composite_contest.contest_id'), primary_key=True)
    __table_args__ = {'extend_existing': True}


class ContestsInCompositeContest(db.Model):
    """
    Class describing a Contests In Composite Contest model.

    ///
    """

    __tablename__ = 'contests_in_composite_contest'

    composite_contest_id = db.Column(db.Integer, db.ForeignKey('composite_contest.contest_id'), primary_key=True)
    contest_id = db.Column(db.Integer, db.ForeignKey('composite_contest.contest_id'), primary_key=True)
    __table_args__ = {'extend_existing': True}


# Tasks models

class TaskVariant(db.Model):
    """
    Class describing a Task variant model.

    variant_id: id of the variant
    variant_number: id of the variant number
    variant_description: description of the variant
    """

    __tablename__ = 'task_variant'

    variant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    variant_number = db.Column(db.Integer)
    variant_description = db.Column(db.Text)
    __table_args__ = {'extend_existing': True}


class TaskInVariant(db.Model):
    """
    Class describing a Task in variant model.

    variant_id: id of the variant
    task_id: id of the task
    """

    __tablename__ = 'task_in_variant'

    variant_id = db.Column(db.Integer, db.ForeignKey('task_variant.variant_id'), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('base_task.task_id'), primary_key=True)

    __table_args__ = {'extend_existing': True}


class Task(db.Model):
    """
    Class describing a Base Task model.

    task_id: id of the task
    num_of_task: number of the task
    image_of_task: image file
    """

    __tablename__ = 'base_task'
    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    num_of_task = db.Column(db.Integer, nullable=False)
    image_of_task = db.Column(db.LargeBinary, nullable=False)
    __table_args__ = {'extend_existing': True}


class PlainTask(db.Model):
    """
    Class describing a Task with plain text model.

    task_id: id of the task
    recommended_answer: recommended for student answer
    """

    __tablename__ = 'plain_task'

    task_id = db.Column(db.Integer, db.ForeignKey('base_task.task_id'), primary_key=True)
    recommended_answer = db.Column(db.Text, nullable=False)
    __table_args__ = {'extend_existing': True}


class RangeTask(db.Model):
    """
    Class describing a Task with range model.

    task_id: id of the task
    start_value: start value of the range of the answer
    end_value: end value of the range of the answer
    """

    __tablename__ = 'range_task'

    task_id = db.Column(db.Integer, db.ForeignKey('base_task.task_id'), primary_key=True)
    start_value = db.Column(db.Text, nullable=False)
    end_value = db.Column(db.Text, nullable=False)
    __table_args__ = {'extend_existing': True}


class MultipleChoiceTask(db.Model):
    """
    Class describing a Task with multiple choice model.

    task_id: id of the task
    correct_answer: correct answer
    """

    __tablename__ = 'multiple_task'

    task_id = db.Column(db.Integer, db.ForeignKey('base_task.task_id'), primary_key=True)
    correct_answer = db.Column(db.String(50), nullable=False)
    __table_args__ = {'extend_existing': True}


class AnswersInMultipleChoiceTask(db.Model):
    """
    Class describing a Multiple answers for the task model.

    task_id: id of the task
    answer: possible answer
    """

    __tablename__ = 'answers_in_multiple_task'

    task_id = db.Column(db.Integer, db.ForeignKey('multiply_task.task_id'), primary_key=True)
    answer = db.Column(db.String(50), primary_key=True)
    __table_args__ = {'extend_existing': True}


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

# debug


#if __name__ == "__main__":
    # db.create_all()
