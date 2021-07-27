"""File with models description for contests and tasks management."""

from contest_data.app import db
from datetime import datetime
import enum

# Constants

DEFAULT_VISIBILITY = False


# Contest models

class Olympiad(db.Model):
    """
    Class describing a Olympiad model.

    olympiad_id: id of olympiad
    description: description of the contest
    rules: rules of the contest
    """

    __tablename__ = 'olympiad'

    olympiad_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    rules = db.Column(db.Text, nullable=False)
    stages = db.relationship('olympiad_stage', lazy='select',
                             backref=db.backref('olympiad', lazy='joined'))


"""
Table describing a Contests In Stage model.

stage_id: id of the stage
contest_id: id of contest
location: address + room or link to online
"""

contestsInStage = db.Table('contests_in_stage',
                           db.Column('stage_id', db.Integer, db.ForeignKey('olympiad_stage.stage_id'),
                                     primary_key=True),
                           db.Column('contest_id', db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True),
                           db.Column('location', db.Text, nullable=False)
                           )


class OlympiadStage(db.Model):
    """
    Class describing a Stage model.

    stage_id: id of the stage
    olympiad_id: id of olympiad
    stage_name: name of the stage
    next_stage_condition: condition to pass to the next stage
    """

    __tablename__ = 'olympiad_stage'

    stage_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    olympiad_id = db.Column(db.Integer, db.ForeignKey('olympiad.olympiad_id'))
    stage_name = db.Column(db.Text, index=True, nullable=False)
    next_stage_condition = db.Column(db.Text, nullable=False)

    contests = db.relationship('contest', secondary=contestsInStage, lazy='subquery',
                               backref=db.backref('olympiad_stage', lazy=True))


class Contest(db.Model):
    """
    Class describing a Contest model.

    contest_id: id of contest
    description: description of the contest
    rules: rules of the contest
    winning_condition: minimum passing scores
    laureate_condition: minimum passing scores
    certificate_template: contest certificate template
    visibility: visibility of the contest
    start_date: start date of contest
    end_date: end date of contest
    """

    __tablename__ = 'contest'

    contest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    rules = db.Column(db.Text, nullable=False)
    winning_condition = db.Column(db.Float, nullable=False)
    laureate_condition = db.Column(db.Float, nullable=False)
    certificate_template = db.Column(db.Text, nullable=True)
    visibility = db.Column(db.Boolean, default=DEFAULT_VISIBILITY, nullable=False)

    start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    variants = db.relationship('variant', lazy='select',
                               backref=db.backref('contest', lazy='joined'))

    users = db.relationship('user_in_contest', lazy='select',
                            backref=db.backref('contest', lazy='joined'))


"""
Class describing a Task in variant model.

variant_id: id of the variant
task_id: id of the task
"""

taskInVariant = db.Table('task_in_variant',
                         db.Column('variant_id', db.Integer, db.ForeignKey('variant.variant_id'), primary_key=True),
                         db.Column('task_id', db.ForeignKey('base_task.task_id'), primary_key=True)
                         )


class Variant(db.Model):
    """
    Class describing a Task variant model.

    variant_id: id of the variant
    contest_id: id of contest
    variant_number: id of the variant number
    variant_description: description of the variant
    """

    __tablename__ = 'variant'

    variant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'))
    variant_number = db.Column(db.Integer)
    variant_description = db.Column(db.Text)

    users = db.relationship('user_in_contest', lazy='select',
                            backref=db.backref('variant', lazy='joined'))

    contests = db.relationship('base_task', secondary=taskInVariant, lazy='subquery',
                               backref=db.backref('variant', lazy=True))


class UserInContest(db.Model):
    """
    Class describing a User in contest model.

    contest_id: id of the contest
    user_id: if of user
    user_status: user status: laureate, winner or custom value
    variant_id: variant connected with current contest
    """

    __tablename__ = 'user_in_contest'
    user_id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True)
    variant_id = db.Column(db.Integer, db.ForeignKey('variant.variant_id'))
    user_status = db.Column(db.Text, nullable=False)


class TaskType(enum.Enum):

    plain_task = 1
    range_task = 2
    multiple_task = 3


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
    image_of_task = db.Column(db.LargeBinary, nullable=True)
    type = db.Column(db.Enum(TaskType))

    plain_tasks = db.relationship('plain_task', lazy='select',
                                  backref=db.backref('base_task', lazy='joined'))
    range_tasks = db.relationship('range_task', lazy='select',
                                  backref=db.backref('base_task', lazy='joined'))
    multiple_tasks = db.relationship('multiple_task', lazy='select',
                                     backref=db.backref('base_task', lazy='joined'))

    __mapper_args__ = {
        'polymorphic_identity': 'base_task',
        'polymorphic_on': type
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

    __mapper_args__ = {
        'polymorphic_identity': 'plain_task',
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
        'polymorphic_identity': 'range_task',
    }


class MultipleChoiceTask(Task):
    """
    Class describing a Task with multiple choice model.

    task_id: id of the task
    """

    __tablename__ = 'multiple_task'

    task_id = db.Column(db.Integer, db.ForeignKey('base_task.task_id'), primary_key=True)
    all_answers_in_multiple_task = db.relationship('answers_in_multiple_task', lazy='select',
                                                   backref=db.backref('multiple_task', lazy='joined'))

    __mapper_args__ = {
        'polymorphic_identity': 'multiple_task',
    }


class AnswersInMultipleChoiceTask(db.Model):
    """
    Class describing a Multiple answers for the task model.

    answer_id: id of answer
    task_id: id of the task
    answer: possible answer
    correct: is answer correct
    """

    __tablename__ = 'answers_in_multiple_task'

    answer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('multiple_task.task_id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
