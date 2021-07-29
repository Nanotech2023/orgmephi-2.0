"""File with models description for contests and tasks management."""

from contest_data.app import db
from datetime import datetime
import enum

# Constants

DEFAULT_VISIBILITY = Truex

class UserStatus(db.Model):
    __tablename__ = 'user_status'

    status_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    status = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {'status_id': self.id, 'status': self.name}

    def update(self, status):
        self.status = status

def add_user_status(db_session, status):
    userStatus = UserStatus(
        status=status
    )
    db_session.add(userStatus)
    db_session.flush()
    return userStatus


class CompositeTypeEnum(enum.Enum):
    Composite = "Composite",
    Simple = "Simple",


composite_type_dict = {composite.value: composite for composite in CompositeTypeEnum}


class OlympiadTypeEnum(enum.Enum):
    Rosatom = "Rosatom",
    Kurchatov = "Kurchatov",
    Other = "Other",


olympiad_type_dict = {type.value: type for type in OlympiadTypeEnum}


class OlympiadSubjectEnum(enum.Enum):
    Math = "Math",
    Physics = "Physics",
    Informatics = "Informatics",


olympiad_subject_dict = {subject.value: subject for subject in OlympiadSubjectEnum}


class TargetClassEnum(enum.Enum):
    class_5 = "5",
    class_6 = "6",
    class_7 = "7",
    class_8 = "8",
    class_9 = "9",
    class_10 = "10",
    class_11 = "11",
    student = "student",


olympiad_target_class_dict = {target.value: target for target in TargetClassEnum}

def add_base_contest(db_session, description, rules, olympiad_type, subject):
    baseContest = BaseContest(
        description=description,
        rules=rules,
        olympiad_type=olympiad_type,
        subject=subject
    )
    db_session.add(baseContest)
    db_session.flush()
    return baseContest

# Contest models
class BaseContest(db.Model):
    """
    Base Class describing a Contest model with meta information.

    base_contest_id: id of base contest

    description: description of the contest
    rules: rules of the contest
    olympiad_type: olympiad type
    subject: subject

    target_class: target class

    """

    __tablename__ = 'base_contest'

    base_contest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    description = db.Column(db.Text, nullable=False)
    rules = db.Column(db.Text, nullable=False)
    olympiad_type = db.Column(db.Enum(OlympiadTypeEnum), nullable=False)
    subject = db.Column(db.Enum(OlympiadSubjectEnum), nullable=False)

    target_classes = db.relationship('target_classes', lazy='select',
                                     backref=db.backref('base_contest', lazy='joined'))
    child_contests = db.relationship('contest', lazy='select',
                                     backref=db.backref('base_contest', lazy='joined'))

    def serialize(self):
        return \
            {
                'base_contest_id': self.base_contest_id,
                'description': self.description,
                'rules': self.rules,
                'olympiad_type': self.olympiad_type,
                'subject': self.subject,
                'target_classes': self.target_classes,
                'child_contests': self.child_contests
            }

    def update(self, description=None, rules=None, olympiad_type=None, subject=None, target_classes=None):
        if description is not None:
            self.description = description
        if rules is not None:
            self.rules = rules
        if olympiad_type is not None:
            self.olympiad_type = olympiad_type
        if subject is not None:
            self.subject = subject
        if target_classes is not None:
            self.target_classes = target_classes


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
    composite_type: composite type
    olympiad_type: olympiad type
    subject: subject
    """

    __tablename__ = 'contest'

    base_contest_id = db.Column(db.Integer, db.ForeignKey('base_contest.contest_id'), primary_key=True)
    contest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    winning_condition = db.Column(db.Float, nullable=False)
    laureate_condition = db.Column(db.Float, nullable=False)
    certificate_template = db.Column(db.Text, nullable=True)
    visibility = db.Column(db.Boolean, default=DEFAULT_VISIBILITY, nullable=False)

    users = db.relationship('user_in_contest', lazy='select',
                            backref=db.backref('contest', lazy='joined'))

    composite_type = db.Column(db.Enum(CompositeTypeEnum), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'base_contest',
        'polymorphic_on': composite_type
    }


def add_simple_contest(db_session, base_contest_id, winning_condition, laureate_condition, certificate_template,
                       visibility, start_date, end_date, previous_contest_id=None, previous_participation_condition=None):
    simpleContest = SimpleContest(
        base_contest_id=base_contest_id,
        winning_condition=winning_condition,
        laureate_condition=laureate_condition,
        certificate_template=certificate_template,
        visibility=visibility,
        start_date=start_date,
        end_date=end_date,
        previous_contest_id=previous_contest_id,
        previous_participation_condition=previous_participation_condition,
    )
    db_session.add(simpleContest)
    db_session.flush()
    return simpleContest


class SimpleContest(BaseContest):
    """
    Simple contest model.

    start_date: start date of contest
    end_date: end date of contest
    """
    __tablename__ = 'simple_contest'

    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True)
    start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    previous_contest_id = db.Column(db.Integer, db.ForeignKey('simple_contest.contest_id'), nullable=True)
    previous_participation_condition = db.Column(db.Text, db.ForeignKey('user_status.status_id'), nullable=True)

    variants = db.relationship('variant', lazy='select',
                               backref=db.backref('simple_contest', lazy='joined'))

    __mapper_args__ = {
        'polymorphic_identity': 'simple_contest',
    }

    def serialize(self):
        return \
            {
                'contest_id': self.contest_id,
                'winning_condition': self.winning_condition,
                'laureate_condition': self.laureate_condition,
                'certificate_template': self.certificate_template,
                'visibility': self.visibility,
                'users': self.users,
                'composite_type': self.composite_type,
                'start_date': self.description.isoformat(),
                'end_date': self.end_date.isoformat(),
                'variants': self.variants,
                'previous_contest_id': self.previous_contest_id,
                'previous_participation_condition': self.previous_participation_condition
            }

    def update(self, start_date=None, end_date=None, variants=None, previous_contest_id=None, previous_participation_condition=None,
            winning_condition=None, laureate_condition=None, certificate_template=None, visibility=None, users=None, composite_type=None):
        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date
        if previous_contest_id is not None:
            self.previous_contest_id = previous_contest_id
        if previous_participation_condition is not None:
            self.previous_participation_condition = previous_participation_condition
        if winning_condition is not None:
            self.winning_condition = winning_condition
        if laureate_condition is not None:
            self.laureate_condition = laureate_condition
        if certificate_template is not None:
            self.certificate_template = certificate_template
        if visibility is not None:
            self.visibility = visibility
        if composite_type is not None:
            self.composite_type = composite_type


def add_composite_contest(db_session, base_contest_id, winning_condition, laureate_condition, certificate_template,
                       visibility):
    compositeContest = CompositeContest(
        base_contest_id=base_contest_id,
        winning_condition=winning_condition,
        laureate_condition=laureate_condition,
        certificate_template=certificate_template,
        visibility=visibility,
    )
    db_session.add(compositeContest)
    db_session.flush()
    return compositeContest


class CompositeContest(BaseContest):
    __tablename__ = 'composite_contest'

    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True)

    stages = db.relationship('stage', lazy='select',
                             backref=db.backref('composite_contest', lazy='joined'))

    def serialize(self):
        return \
            {
                'contest_id': self.contest_id,
                'winning_condition': self.winning_condition,
                'laureate_condition': self.laureate_condition,
                'certificate_template': self.certificate_template,
                'visibility': self.visibility,
                'users': self.users,
                'stages': self.stages,
                'composite_type': self.composite_type
            }

    def update(self, winning_condition=None, laureate_condition=None, certificate_template=None, visibility=None, users=None, composite_type=None):
        if winning_condition is not None:
            self.winning_condition = winning_condition
        if laureate_condition is not None:
            self.laureate_condition = laureate_condition
        if certificate_template is not None:
            self.certificate_template = certificate_template
        if visibility is not None:
            self.visibility = visibility
        if composite_type is not None:
            self.composite_type = composite_type

    __mapper_args__ = {
        'polymorphic_identity': 'composite_contest',
    }



class TargetClass(db.Model):
    """
    Table describing a Target class of olympiad.
    """

    __tablename__ = 'target_classes'

    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True)
    target_class = db.Column(db.Enum(TargetClassEnum), primary_key=True)

    def serialize(self):
        return {'contest_id': self.contest_id, 'target_class': self.target_class}

    def update(self, target_class):
        self.target_class = target_class

def add_target_class(db_session, target_class):
    target_class = TargetClass(
        target_class=target_class
    )
    db_session.add(target_class)
    db_session.flush()
    return target_class

"""
Table describing a Contests In Stage model.

stage_id: id of the stage
contest_id: id of contest
location: address + room or link to online
"""

contestsInStage = db.Table('contests_in_stage',
                           db.Column('stage_id', db.Integer, db.ForeignKey('stage.stage_id'),
                                     primary_key=True),
                           db.Column('contest_id', db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True),
                           db.Column('location', db.Text, nullable=False)
                           )

def add_contest_in_stage(db_session, stage_id, contest_id, location):
    contestsInStageObject = contestsInStage(
        stage_id=stage_id,
        contest_id=contest_id,
        location=location,
    )
    db_session.add(contestsInStageObject)
    db_session.flush()
    return contestsInStageObject


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

    contests = db.relationship('contest', secondary=contestsInStage, lazy='subquery',
                               backref=db.backref('stage', lazy=True))

    def serialize(self):
        return \
            {
                'stage_id': self.stage_id,
                'olympiad_id': self.olympiad_id,
                'stage_name': self.stage_name,
                'next_stage_condition': self.next_stage_condition,
                'contests': self.contests
            }

    def update(self, stage_name=None, next_stage_condition=None, contests=None):
        if stage_name is not None:
            self.stage_name = stage_name
        if next_stage_condition is not None:
            self.next_stage_condition = next_stage_condition


def add_stage(db_session, olympiad_id, stage_name, next_stage_condition):
    stage = Stage(
        olympiad_id=olympiad_id,
        stage_name=stage_name,
        next_stage_condition=next_stage_condition
    )
    db_session.add(stage)
    db_session.flush()
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


def add_task_in_Variant(db_session, variant_id, task_id):
    taskInVariantObject = taskInVariant(
        variant_id=variant_id,
        task_id=task_id,
    )
    db_session.add(taskInVariantObject)
    db_session.flush()
    return taskInVariantObject


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

    tasks = db.relationship('base_task', secondary=taskInVariant, lazy='subquery',
                               backref=db.backref('variant', lazy=True))


    def serialize(self):
        return \
            {
                'variant_id': self.variant_id,
                'contest_id': self.contest_id,
                'variant_number': self.variant_number,
                'variant_description': self.variant_description,
                'users': self.users,
                'tasks': self.tasks
            }

    def update(self, variant_number=None, variant_description=None):
        if variant_number is not None:
            self.variant_number = variant_number
        if variant_description is not None:
            self.variant_description = variant_description



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
    user_status = db.Column(db.Text, db.ForeignKey('user_status.status_id'))



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


    def serialize(self):
        return \
            {
                'num_of_task': self.num_of_task,
                'image_of_task': self.image_of_task,
                'type': self.type,
                'plain_tasks': self.plain_tasks,
                'multiple_tasks': self.multiple_tasks,
                'recommended_answer': self.recommended_answer,
                'range_tasks': self.range_tasks
            }


    def update(self, num_of_task=None, image_of_task=None, recommended_answer=None):
        if num_of_task is not None:
            self.num_of_task = num_of_task
        if image_of_task is not None:
            self.image_of_task = image_of_task
        if recommended_answer is not None:
            self.recommended_answer = recommended_answer



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

    def serialize(self):
        return \
            {
                'num_of_task': self.num_of_task,
                'image_of_task': self.image_of_task,
                'type': self.type,
                'plain_tasks': self.plain_tasks,
                'multiple_tasks': self.multiple_tasks,
                'recommended_answer': self.recommended_answer,
                'start_value': self.start_value,
                'end_value': self.end_value,
                'range_tasks': self.range_tasks
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

    def serialize(self):
        return \
            {
                'num_of_task': self.num_of_task,
                'image_of_task': self.image_of_task,
                'type': self.type,
                'plain_tasks': self.plain_tasks,
                'multiple_tasks': self.multiple_tasks,
                'all_answers_in_multiple_task': self.all_answers_in_multiple_task,
                'range_tasks': self.range_tasks
            }

    def update(self, num_of_task=None, image_of_task=None, all_answers_in_multiple_task=None):
        if num_of_task is not None:
            self.num_of_task = num_of_task
        if image_of_task is not None:
            self.image_of_task = image_of_task
        if all_answers_in_multiple_task is not None:
            self.all_answers_in_multiple_task = all_answers_in_multiple_task

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

    def update(self, answer=None, correct=None):
        if answer is not None:
            self.answer = answer
        if correct is not None:
            self.correct = correct