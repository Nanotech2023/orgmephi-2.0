"""File with models description for contests and tasks management."""

from datetime import datetime
import enum
from common import get_current_db
from common.util import db_get_or_raise

db = get_current_db()

DEFAULT_VISIBILITY = True


class UserStatusEnum(enum.Enum):
    Participant = "Participant"
    Laureate = "Laureate"
    Winner = "Winner"


user_status_dict = {status.value: status for status in UserStatusEnum}


class OlympiadSubjectEnum(enum.Enum):
    Math = "Math"
    Physics = "Physics"
    Informatics = "Informatics"


olympiad_subject_dict = {subject.value: subject for subject in OlympiadSubjectEnum}


class TargetClassEnum(enum.Enum):
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
    """

    __tablename__ = 'olympiad_type'

    olympiad_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    olympiad_type = db.Column(db.Text, nullable=False)

    contests = db.relationship('BaseContest', lazy='select',
                               backref=db.backref('olympiad_type', lazy='joined'))

    def serialize(self):
        return \
            {
                'olympiad_type_id': self.olympiad_type_id,
                'olympiad_type': self.olympiad_type,
            }


def add_base_contest(db_session, name, laureate_condition, winning_condition, description, rules, olympiad_type_id,
                     subject, certificate_template):
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
    description: description of the contest
    rules: rules of the contest
    certificate_template: contest certificate template

    winning_condition: minimum passing scores
    laureate_condition: minimum passing scores

    composite_type: composite type
    olympiad_type: olympiad type
    subject: subject
    target_class: target class

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

    target_classes = db.relationship('TargetClass', lazy='select',
                                     backref=db.backref('base_contest', lazy='joined'), cascade="all, delete-orphan")
    child_contests = db.relationship('Contest', lazy='select',
                                     backref=db.backref('base_contest', lazy='joined'), cascade="all, delete-orphan")

    def serialize(self):
        return \
            {
                'base_contest_id': self.base_contest_id,
                'name': self.name,
                'description': self.description,
                'rules': self.rules,
                'olympiad_type_id': self.olympiad_type_id,
                'subject': self.subject.value,
                'winning_condition': self.winning_condition,
                'laureate_condition': self.laureate_condition,
                'target_classes': [target.target_class.value for target in self.target_classes],
            }

    def update(self, name=None, certificate_template=None,
               description=None,
               rules=None,
               olympiad_type_id=None,
               subject=None,
               winning_condition=None,
               laureate_condition=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if winning_condition is not None:
            self.winning_condition = winning_condition
        if laureate_condition is not None:
            self.laureate_condition = laureate_condition
        if rules is not None:
            self.rules = rules
        if certificate_template is not None:
            self.certificate_template = certificate_template
        if olympiad_type_id is not None:
            self.olympiad_type_id = olympiad_type_id
        if subject is not None:
            self.subject = subject


class TargetClass(db.Model):
    """
    Table describing a Target class of olympiad.
    """

    __tablename__ = 'target_class'

    contest_id = db.Column(db.Integer, db.ForeignKey('base_contest.base_contest_id'), primary_key=True)
    target_class = db.Column(db.Enum(TargetClassEnum), primary_key=True)

    def serialize(self):
        return {'contest_id': self.contest_id,
                'target_class': self.target_class.value}


def add_target_class(db_session, contest_id, target_class_):
    target_class = TargetClass(
        contest_id=contest_id,
        target_class=target_class_
    )
    db_session.add(target_class)
    return target_class


class ContestTypeEnum(enum.Enum):
    Contest = "Contest"
    SimpleContest = "SimpleContest"
    CompositeContest = "CompositeContest"


class Contest(db.Model):
    """
    Class describing a Contest model.

    base_contest_id: id of base contest

    contest_id: id of contest
    visibility: visibility of the contest
    composite_type: composite type

    subject: subject
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

    base_contest_id: id of base contest

    contest_id: id of contest
    visibility: visibility of the contest
    start_date: start date of contest
    end_date: end date of contest
    location: location of the olympiad
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

    __mapper_args__ = {
        'polymorphic_identity': ContestTypeEnum.SimpleContest,
    }

    def change_previous(self, previous_contest_id=None, previous_participation_condition=None):
        if previous_contest_id is not None:
            self.previous_contest_id = previous_contest_id
        if previous_participation_condition is not None:
            self.previous_participation_condition = previous_participation_condition

    def serialize(self):
        return \
            {
                'contest_id': self.contest_id,
                'visibility': self.visibility,
                'composite_type': self.composite_type.value,
                'start_date': self.start_date.isoformat(),
                'end_date': self.end_date.isoformat(),
                'location': self.location,
            }

    def update(self, start_date=None, end_date=None, previous_contest_id=None,
               previous_participation_condition=None, visibility=None, composite_type=None, location=None):
        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date
        if previous_contest_id is not None:
            self.previous_contest_id = previous_contest_id
        if previous_participation_condition is not None:
            self.previous_participation_condition = previous_participation_condition
        if visibility is not None:
            self.visibility = visibility
        if composite_type is not None:
            self.composite_type = composite_type
        if location is not None:
            self.location = location


def add_composite_contest(db_session, visibility, base_contest_id=None):
    composite_contest = CompositeContest(
        base_contest_id=base_contest_id,
        visibility=visibility,
    )
    db_session.add(composite_contest)
    return composite_contest


class CompositeContest(Contest):
    __tablename__ = 'composite_contest'

    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True)

    stages = db.relationship('Stage', lazy='select',
                             backref=db.backref('composite_contest', lazy='joined'))

    def serialize(self):
        return \
            {
                'contest_id': self.contest_id,
                'composite_type': self.composite_type.value,
                'visibility': self.visibility,
            }

    def update(self, visibility=None, composite_type=None):
        if visibility is not None:
            self.visibility = visibility
        if composite_type is not None:
            self.composite_type = composite_type

    __mapper_args__ = {
        'polymorphic_identity': ContestTypeEnum.CompositeContest,
    }


"""
Table describing a Contests In Stage model.

stage_id: id of the stage
contest_id: id of contest
location: address + room or link to online
"""

contestsInStage = db.Table('contests_in_stage',
                           db.Column('stage_id', db.Integer, db.ForeignKey('stage.stage_id'),
                                     primary_key=True),
                           db.Column('contest_id', db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True)
                           )


class Stage(db.Model):
    """
    Class describing a Stage model.

    stage_id: id of the stage
    olympiad_id: id of olympiad
    stage_name: name of the stage
    next_stage_condition: condition to pass to the next stage
    """

    __tablename__ = 'stage'

    stage_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    olympiad_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'))
    stage_name = db.Column(db.Text, index=True, nullable=False)
    next_stage_condition = db.Column(db.Text, nullable=False)

    contests = db.relationship('Contest', secondary=contestsInStage, lazy='subquery',
                               backref=db.backref('stage', lazy=True))

    def serialize(self):
        return \
            {
                'stage_id': self.stage_id,
                'olympiad_id': self.olympiad_id,
                'stage_name': self.stage_name,
                'next_stage_condition': self.next_stage_condition,
            }

    def update(self, stage_name=None, next_stage_condition=None):
        if stage_name is not None:
            self.stage_name = stage_name
        if next_stage_condition is not None:
            self.next_stage_condition = next_stage_condition


def add_stage(db_session, stage_name, next_stage_condition, olympiad_id=None):
    stage = Stage(
        stage_name=stage_name,
        next_stage_condition=next_stage_condition,
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

    def serialize(self):
        return \
            {
                'variant_id': self.variant_id,
                'contest_id': self.contest_id,
                'variant_number': self.variant_number,
                'variant_description': self.variant_description,
            }

    def update(self, contest_id=None, variant_number=None, variant_description=None):
        if contest_id is not None:
            self.contest_id = contest_id
        if variant_number is not None:
            self.variant_number = variant_number
        if variant_description is not None:
            self.variant_description = variant_description


def add_user_in_contest(db_session, user_id, contest_id, variant_id=None, user_status=None):
    user = UserInContest(
        user_id=user_id,
        contest_id=contest_id,
        variant_id=variant_id,
        user_status=user_status,
    )
    db_session.add(user)
    return user


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
    user_status = db.Column(db.Enum(UserStatusEnum))

    def serialize(self):
        return \
            {
                'user_id': self.user_id,
                'user_status': self.user_status.value,
                'variant_id': self.variant_id
            }

    def update(self, contest_id=None, variant_id=None, user_status=None):
        if contest_id is not None:
            self.contest_id = contest_id
        if variant_id is not None:
            self.variant_id = variant_id
        if user_status is not None:
            self.user_status = user_status


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


def add_plain_task(db_session, num_of_task, image_of_task, recommended_answer):
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

    def serialize(self):
        return \
            {
                'task_id': self.task_id,
                'num_of_task': self.num_of_task,
                'recommended_answer': self.recommended_answer,
            }

    def update(self, num_of_task=None, image_of_task=None, recommended_answer=None):
        if num_of_task is not None:
            self.num_of_task = num_of_task
        if image_of_task is not None:
            self.image_of_task = image_of_task
        if recommended_answer is not None:
            self.recommended_answer = recommended_answer


def add_range_task(db_session, num_of_task, image_of_task, start_value, end_value):
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

    def serialize(self):
        return \
            {
                'task_id': self.task_id,
                'num_of_task': self.num_of_task,
                'start_value': self.start_value,
                'end_value': self.end_value,
            }

    def update(self, num_of_task=None, image_of_task=None, start_value=None, end_value=None):
        if num_of_task is not None:
            self.num_of_task = num_of_task
        if image_of_task is not None:
            self.image_of_task = image_of_task
        if start_value is not None:
            self.start_value = start_value
        if end_value is not None:
            self.end_value = end_value


def add_multiple_task(db_session, num_of_task, image_of_task):
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
    """

    __tablename__ = 'multiple_task'

    task_id = db.Column(db.Integer, db.ForeignKey('base_task.task_id'), primary_key=True)
    all_answers_in_multiple_task = db.relationship('AnswersInMultipleChoiceTask', lazy='select',
                                                   backref=db.backref('multiple_task', lazy='joined'),
                                                   cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': TaskTypeEnum.MultipleChoiceTask,
    }

    def serialize(self):
        return \
            {
                'task_id': self.task_id,
                'num_of_task': self.num_of_task,
                'all_answers_in_multiple_task': [answer.serialize() for answer in self.all_answers_in_multiple_task],
            }

    def update(self, num_of_task=None, image_of_task=None):
        if num_of_task is not None:
            self.num_of_task = num_of_task
        if image_of_task is not None:
            self.image_of_task = image_of_task


def add_answer_to_multiple_task(db_session, task_id, answer, correct):
    answers_in_multiple_choice_task = AnswersInMultipleChoiceTask(
        task_id=task_id,
        answer=answer,
        correct=correct
    )
    db_session.add(answers_in_multiple_choice_task)


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

    def serialize(self):
        return \
            {
                'answer_id': self.answer_id,
                'answer': self.answer,
                'correct': self.correct
            }

    def update(self, answer=None, correct=None):
        if answer is not None:
            self.answer = answer
        if correct is not None:
            self.correct = correct
