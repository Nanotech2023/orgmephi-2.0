import enum

from common import get_current_db
from common.media_types import TaskImage, Json

db = get_current_db()


class TaskAnswerTypeEnum(enum.Enum):
    File = "File"
    Text = "Text"


class TaskTypeEnum(enum.Enum):
    PlainTask = "PlainTask"
    RangeTask = "RangeTask"
    MultipleChoiceTask = "MultipleChoiceTask"
    BaseTask = "BaseTask"


class TaskPool(db.Model):
    """
    Task pool

    task_pool_id: id of the task pool
    base_contest_id: id of the base contest
    name: task pool name
    year: year of the task pool usage
    orig_task_points: recommended task points
    """

    __tablename__ = "task_pool"
    task_pool_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    base_contest_id = db.Column(db.Integer, db.ForeignKey('base_contest.base_contest_id'), nullable=True)
    name = db.Column(db.Text)
    year = db.Column(db.Integer)
    orig_task_points = db.Column(db.Integer)

    tasks = db.relationship('Task', backref='task_pool', lazy='dynamic')


"""
Table describing a Task Pool In Contest Task.

stage_id: id of the stage
contest_id: id of contest
"""

taskPoolInContestTask = db.Table('task_pool_in_contest_task',
                                 db.Column('task_pool_id', db.Integer, db.ForeignKey('task_pool.task_pool_id'),
                                           primary_key=True),
                                 db.Column('contest_task_id', db.Integer, db.ForeignKey('contest_task.contest_task_id'),
                                           primary_key=True)
                                 )


class ContestTask(db.Model):
    """
    Task pool

    contest_task_id: id of the task pool
    contest_id: id of the contest
    num: num of the task
    task_points: task points
    """

    __tablename__ = "contest_task"
    contest_task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.base_contest_id'), nullable=True)
    num = db.Column(db.Integer)
    task_points = db.Column(db.Integer)

    task_pools = db.relationship('TaskPool', secondary=taskPoolInContestTask, lazy='subquery',
                                 backref=db.backref('contest_task', lazy=True))


class ContestTaskInVariant(db.Model):
    """
    Contest Task In Variant

    contest_task_id: id of the task pool
    contest_id: id of the contest
    num: num of the task
    task_points: task points
    """

    __tablename__ = "contest_task_in_variant"
    contest_task_id = db.Column(db.Integer, db.ForeignKey('contest_task.contest_task_id'), primary_key=True)
    variant_id = db.Column(db.Integer, db.ForeignKey('variant.variant_id'), primary_key=True)
    base_task_id = db.Column(db.Integer, db.ForeignKey('base_task.task_id'))


class Task(db.Model):
    """
    Class describing a Base Task model.

    task_id: id of the task
    num_of_task: number of the task
    image_of_task: image file
    task_type: task type for inheritance
    """

    __tablename__ = 'base_task'
    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    task_pool_id = db.Column(db.Integer, db.ForeignKey('task_pool.task_pool_id'))

    image_of_task = db.Column(TaskImage.as_mutable(Json))

    task_type = db.Column(db.Enum(TaskTypeEnum))

    __mapper_args__ = {
        'polymorphic_identity': TaskTypeEnum.BaseTask,
        'polymorphic_on': task_type
    }


def add_plain_task(db_session, recommended_answer, image_of_task=None,
                   answer_type=TaskAnswerTypeEnum.Text):
    """
    Create new plain task object
    """
    task = PlainTask(
        image_of_task=image_of_task,
        recommended_answer=recommended_answer,
        answer_type=answer_type,
    )
    db_session.add(task)
    return task


class PlainTask(Task):
    """
    Class describing a Task with plain text model.

    task_id: id of the task
    recommended_answer: recommended for student answer
    """

    __tablename__ = 'plain_task'

    task_id = db.Column(db.Integer, db.ForeignKey('base_task.task_id'), primary_key=True)
    recommended_answer = db.Column(db.Text, nullable=False)
    answer_type = db.Column(db.Enum(TaskAnswerTypeEnum), default=TaskAnswerTypeEnum.Text)

    __mapper_args__ = {
        'polymorphic_identity': TaskTypeEnum.PlainTask,
        'with_polymorphic': '*'
    }


def add_range_task(db_session, start_value, end_value, image_of_task=None):
    """
    Create new range task object
    """
    task = RangeTask(
        image_of_task=image_of_task,
        start_value=start_value,
        end_value=end_value,
    )
    db_session.add(task)
    return task


class RangeTask(Task):
    """
    Class describing a Task with range model.

    task_id: id of the task
    start_value: start value of the range of the answer
    end_value: end value of the range of the answer
    """

    __tablename__ = 'range_task'

    task_id = db.Column(db.Integer, db.ForeignKey('base_task.task_id'), primary_key=True)
    start_value = db.Column(db.Float, nullable=False)
    end_value = db.Column(db.Float, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': TaskTypeEnum.RangeTask,
        'with_polymorphic': '*'
    }


def add_multiple_task(db_session, image_of_task=None):
    """
    Create new multiple task object
    """
    task = MultipleChoiceTask(
        image_of_task=image_of_task,
    )
    db_session.add(task)
    return task


class MultipleChoiceTask(Task):
    """
    Class describing a Task with multiple choice model.

    task_id: id of the task
    answers: answers on multiple tasks
    """

    __tablename__ = 'multiple_task'

    task_id = db.Column(db.Integer, db.ForeignKey('base_task.task_id'), primary_key=True)
    answers = db.Column(db.PickleType)

    __mapper_args__ = {
        'polymorphic_identity': TaskTypeEnum.MultipleChoiceTask,
        'with_polymorphic': '*'
    }


class Variant(db.Model):
    """
    Class describing a Task variant model.

    variant_id: id of the variant
    contest_id: id of contest
    variant_number: id of the variant number
    variant_description: description of the variant

    users: users
    tasks: tasks
    """

    __tablename__ = 'variant'

    variant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    contest_id = db.Column(db.Integer, db.ForeignKey('simple_contest.contest_id'))
    variant_number = db.Column(db.Integer)
    variant_description = db.Column(db.Text)

    users = db.relationship('UserInContest', lazy='dynamic', backref='variant')
    contest_tasks_in_variant = db.relationship('ContestTaskInVariant', lazy='dynamic', backref='variant')


def add_variant(db_session, variant_number=None, variant_description=None, contest_id=None):
    """
    Create new variant object
    """
    variant = Variant(
        contest_id=contest_id,
        variant_number=variant_number,
        variant_description=variant_description,
    )
    db_session.add(variant)
    return variant
