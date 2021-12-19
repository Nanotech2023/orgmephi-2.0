import enum

from sqlalchemy.ext.hybrid import hybrid_property

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
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'), nullable=True)
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
    task_id = db.Column(db.Integer, db.ForeignKey('base_task.task_id'))

    task = db.relationship('Task')
    contest_task = db.relationship('ContestTask')


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
    name = db.Column(db.Text)

    image_of_task = db.Column(TaskImage.as_mutable(Json))

    task_type = db.Column(db.Enum(TaskTypeEnum))

    @hybrid_property
    def right_answer(self):
        from contest.tasks.models import Contest
        from common.util import db_get_one_or_none
        contest: Contest = db_get_one_or_none(Contest, "contest_id", self.response.contest_id)
        if contest.show_answer_after_contest:
            if self.task_type.value == "PlainTask":
                task: PlainTask = db_get_one_or_none(PlainTask, 'task_id', self.task_id)
                return {'answer': task.recommended_answer}
            elif self.task_type.value == "RangeTask":
                task: RangeTask = db_get_one_or_none(RangeTask, 'task_id', self.task_id)
                return {
                    'start_value': task.start_value,
                    'end_value': task.end_value,
                }
            elif self.task_type.value == "MultipleChoiceTask":
                task: MultipleChoiceTask = db_get_one_or_none(MultipleChoiceTask, 'task_id', self.task_id)
                right_answers = [elem['answer'] for elem in task.answers if elem['is_right_answer']]
                return {'answers': right_answers}

    __mapper_args__ = {
        'polymorphic_identity': TaskTypeEnum.BaseTask,
        'polymorphic_on': task_type
    }


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

    users: users
    tasks: tasks
    """

    __tablename__ = 'variant'

    variant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    contest_id = db.Column(db.Integer, db.ForeignKey('simple_contest.contest_id'))
    variant_number = db.Column(db.Integer)

    users = db.relationship('UserInContest', lazy='dynamic', backref='variant')
    contest_tasks_in_variant = db.relationship('ContestTaskInVariant', lazy='dynamic', backref='variant')
