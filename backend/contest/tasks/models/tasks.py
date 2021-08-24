import enum

from common import get_current_db

db = get_current_db()


class TaskTypeEnum(enum.Enum):
    PlainTask = "PlainTask"
    RangeTask = "RangeTask"
    MultipleChoiceTask = "MultipleChoiceTask"
    BaseTask = "BaseTask"


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
    num_of_task = db.Column(db.Integer, nullable=False)

    image_of_task = db.Column(db.LargeBinary, nullable=True)

    show_answer_after_contest = db.Column(db.Boolean, nullable=True)
    task_points = db.Column(db.Integer, nullable=True)

    task_type = db.Column(db.Enum(TaskTypeEnum))

    __mapper_args__ = {
        'polymorphic_identity': TaskTypeEnum.BaseTask,
        'polymorphic_on': task_type
    }


def add_plain_task(db_session, num_of_task, recommended_answer, image_of_task=None,
                   task_points=None, show_answer_after_contest=None):
    """
    Create new plain task object
    """
    task = PlainTask(
        num_of_task=num_of_task,
        image_of_task=image_of_task,
        show_answer_after_contest=show_answer_after_contest,
        task_points=task_points,
        recommended_answer=recommended_answer,
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

    __mapper_args__ = {
        'polymorphic_identity': TaskTypeEnum.PlainTask,
    }


def add_range_task(db_session, num_of_task, start_value, end_value, image_of_task=None,
                   task_points=None, show_answer_after_contest=None):
    """
    Create new range task object
    """
    task = RangeTask(
        num_of_task=num_of_task,
        image_of_task=image_of_task,
        show_answer_after_contest=show_answer_after_contest,
        task_points=task_points,
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
    }


def add_multiple_task(db_session, num_of_task, image_of_task=None,
                      task_points=None, show_answer_after_contest=None):
    """
    Create new multiple task object
    """
    task = MultipleChoiceTask(
        num_of_task=num_of_task,
        image_of_task=image_of_task,
        show_answer_after_contest=show_answer_after_contest,
        task_points=task_points,
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
    }
