"""File with models description for contests and tasks management."""

from datetime import datetime
import enum
from common import get_current_db

db = get_current_db()

DEFAULT_VISIBILITY = True


class UserStatusEnum(enum.Enum):
    """
    Enum for user statuses
    """
    Participant = "Participant"
    Laureate = "Laureate"
    Winner = "Winner"


user_status_dict = {status.value: status for status in UserStatusEnum}


class OlympiadSubjectEnum(enum.Enum):
    """
    Enum for olympiad subject
    """
    Math = "Math"
    Physics = "Physics"
    Informatics = "Informatics"


olympiad_subject_dict = {subject.value: subject for subject in OlympiadSubjectEnum}


class TargetClassEnum(enum.Enum):
    """
    Enum for olympiad target classes
    """
    class_5 = "5"
    class_6 = "6"
    class_7 = "7"
    class_8 = "8"
    class_9 = "9"
    class_10 = "10"
    class_11 = "11"
    student = "student"


olympiad_target_class_dict = {target.value: target for target in TargetClassEnum}


def add_olympiad_type(db_session, olympiad_type):
    """
    Create new olympiad type object
    """
    olympiad = OlympiadType(
        olympiad_type=olympiad_type,
    )
    db_session.add(olympiad)
    return olympiad


class OlympiadType(db.Model):
    """
    This class describing olympiad type (ex:Росатом).

    olympiad_type_id: id of olympiad type
    olympiad_type: olympiad type

    contests: contest in olympiad
    """

    __tablename__ = 'olympiad_type'

    olympiad_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    olympiad_type = db.Column(db.Text, nullable=False, unique=True)

    contests = db.relationship('BaseContest', lazy='select',
                               backref=db.backref('olympiad_type', lazy='joined'))


def add_base_contest(db_session, name, laureate_condition, winning_condition, description, rules, olympiad_type_id,
                     subject, certificate_template):
    """
    Create new base content object
    """
    base_contest = BaseContest(
        description=description,
        name=name,
        certificate_template=certificate_template,
        rules=rules,
        winning_condition=winning_condition,
        laureate_condition=laureate_condition,
        olympiad_type_id=olympiad_type_id,
        subject=subject
    )
    db_session.add(base_contest)
    return base_contest


# Contest models
class BaseContest(db.Model):
    """
    Base Class describing a Contest model with meta information.

    base_contest_id: id of base contest

    name: name of base contest
    rules: rules of the contest
    description: description of the contest
    olympiad_type_id: olympiad type id
    subject: subject
    certificate_template: contest certificate template

    winning_condition: minimum passing scores
    laureate_condition: minimum passing scores

    target_class: target class
    child_contests: child contests
    """

    __tablename__ = 'base_contest'

    base_contest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    name = db.Column(db.Text, nullable=False)
    rules = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    olympiad_type_id = db.Column(db.Integer, db.ForeignKey('olympiad_type.olympiad_type_id'), nullable=False)
    subject = db.Column(db.Enum(OlympiadSubjectEnum), nullable=False)
    certificate_template = db.Column(db.Text, nullable=True)

    winning_condition = db.Column(db.Float, nullable=False)
    laureate_condition = db.Column(db.Float, nullable=False)

    target_classes = db.Column(db.PickleType)

    child_contests = db.relationship('Contest', lazy='select',
                                     backref=db.backref('base_contest', lazy='joined'), cascade="all, delete-orphan")


class ContestTypeEnum(enum.Enum):
    Contest = "Contest"
    SimpleContest = "SimpleContest"
    CompositeContest = "CompositeContest"


class Contest(db.Model):
    """
    Class describing a Contest model.

    base_contest_id: id of base contest

    contest_id: id of contest
    composite_type: composite type
    visibility: visibility of the contest

    users: users
    """

    __tablename__ = 'contest'

    base_contest_id = db.Column(db.Integer, db.ForeignKey('base_contest.base_contest_id'))

    contest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    composite_type = db.Column(db.Enum(ContestTypeEnum))
    visibility = db.Column(db.Boolean, default=DEFAULT_VISIBILITY, nullable=False)

    users = db.relationship('UserInContest', lazy='dynamic',
                            backref=db.backref('contest', lazy='joined'))

    __mapper_args__ = {
        'polymorphic_identity': ContestTypeEnum.Contest,
        'polymorphic_on': composite_type
    }


def add_simple_contest(db_session,
                       visibility, start_date, end_date, previous_contest_id=None,
                       previous_participation_condition=None, location=None, base_contest_id=None):
    """
    Create new simple contest object
    """
    simple_contest = SimpleContest(
        base_contest_id=base_contest_id,
        visibility=visibility,
        start_date=start_date,
        end_date=end_date,
        previous_contest_id=previous_contest_id,
        previous_participation_condition=previous_participation_condition,
        location=location,
    )
    db_session.add(simple_contest)
    return simple_contest


class SimpleContest(Contest):
    """
    Simple contest model.

    contest_id: id of contest
    start_date: start date of contest
    end_date: end date of contest
    location: location of the olympiad

    previous_contest_id: previous contest id
    previous_participation_condition: previous participation condition

    variants: variants
    next_contest: next contests

    """
    __tablename__ = 'simple_contest'

    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True)
    start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    location = db.Column(db.Text, index=True, nullable=True)

    previous_contest_id = db.Column(db.Integer, db.ForeignKey('simple_contest.contest_id'), nullable=True)
    previous_participation_condition = db.Column(db.Enum(UserStatusEnum))

    variants = db.relationship('Variant', lazy='dynamic',
                               backref=db.backref('simple_contest', lazy='joined'))

    next_contests = db.relationship('SimpleContest',
                                    foreign_keys=[previous_contest_id])

    __mapper_args__ = {
        'polymorphic_identity': ContestTypeEnum.SimpleContest,
    }

    def change_previous(self, previous_contest_id=None, previous_participation_condition=None):
        if previous_contest_id is not None:
            self.previous_contest_id = previous_contest_id
        if previous_participation_condition is not None:
            self.previous_participation_condition = previous_participation_condition


def add_composite_contest(db_session, visibility, base_contest_id=None):
    """
    Create new composite contest object
    """
    composite_contest = CompositeContest(
        base_contest_id=base_contest_id,
        visibility=visibility,
    )
    db_session.add(composite_contest)
    return composite_contest


class CompositeContest(Contest):
    """
    Simple contest model

    contest_id: id of contest

    stages: stages
    """
    __tablename__ = 'composite_contest'

    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True)

    stages = db.relationship('Stage', lazy='select',
                             backref=db.backref('composite_contest', lazy='joined'))

    __mapper_args__ = {
        'polymorphic_identity': ContestTypeEnum.CompositeContest,
    }


"""
Table describing a Contests In Stage model.

stage_id: id of the stage
contest_id: id of contest
"""

contestsInStage = db.Table('contests_in_stage',
                           db.Column('stage_id', db.Integer, db.ForeignKey('stage.stage_id'),
                                     primary_key=True),
                           db.Column('contest_id', db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True)
                           )


class StageConditionEnum(enum.Enum):
    No = "No"
    And = "And"
    Or = "Or"


class Stage(db.Model):
    """
    Class describing a Stage model.

    stage_id: id of the stage
    olympiad_id: id of olympiad
    stage_name: name of the stage
    stage_num: name of the stage

    this_stage_condition: condition to pass to the next stage

    contests: contests
    """

    __tablename__ = 'stage'

    stage_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    olympiad_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'))
    stage_name = db.Column(db.Text, index=True, nullable=False)
    stage_num = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.Enum(StageConditionEnum), nullable=True)
    this_stage_condition = db.Column(db.Text, nullable=False)

    contests = db.relationship('Contest', secondary=contestsInStage, lazy='subquery',
                               backref=db.backref('stage', lazy=True))


def add_stage(db_session, stage_name, condition, stage_num, this_stage_condition, olympiad_id=None):
    """
    Create new stage object
    """
    stage = Stage(
        stage_name=stage_name,
        stage_num=stage_num,
        condition=condition,
        this_stage_condition=this_stage_condition,
        olympiad_id=olympiad_id,
    )
    db_session.add(stage)
    return stage


"""
Class describing a Task in variant model.

variant_id: id of the variant
task_id: id of the task
"""

taskInVariant = db.Table('task_in_variant',
                         db.Column('variant_id', db.Integer, db.ForeignKey('variant.variant_id'), primary_key=True),
                         db.Column('task_id', db.ForeignKey('base_task.task_id'), primary_key=True)
                         )


def add_variant(db_session, variant_number, variant_description, contest_id=None):
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
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'))
    variant_number = db.Column(db.Integer)
    variant_description = db.Column(db.Text)

    users = db.relationship('UserInContest', lazy='select',
                            backref=db.backref('variant', lazy='joined'))

    tasks = db.relationship('Task', secondary=taskInVariant, lazy='subquery',
                            backref=db.backref('variant', lazy=True))


class UserInContest(db.Model):
    """
    Class describing a User in contest model.

    user_id: if of user
    contest_id: id of the contest
    variant_id: variant connected with current contest
    user_status: user status: laureate, winner or custom value
    """

    __tablename__ = 'user_in_contest'
    user_id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True)
    variant_id = db.Column(db.Integer, db.ForeignKey('variant.variant_id'))
    user_status = db.Column(db.Enum(UserStatusEnum))


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
    task_type = db.Column(db.Enum(TaskTypeEnum))

    __mapper_args__ = {
        'polymorphic_identity': TaskTypeEnum.BaseTask,
        'polymorphic_on': task_type
    }

    def serialize_image(self):
        return \
            {
                'task_id': self.task_id,
                'image_of_task': self.image_of_task
            }


def add_plain_task(db_session, num_of_task, recommended_answer, image_of_task=None):
    """
    Create new plain task object
    """
    task = PlainTask(
        num_of_task=num_of_task,
        image_of_task=image_of_task,
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


def add_range_task(db_session, num_of_task, start_value, end_value, image_of_task=None):
    """
    Create new range task object
    """
    task = RangeTask(
        num_of_task=num_of_task,
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
    }


def add_multiple_task(db_session, num_of_task, image_of_task=None):
    """
    Create new multiple task object
    """
    task = MultipleChoiceTask(
        num_of_task=num_of_task,
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
    }
