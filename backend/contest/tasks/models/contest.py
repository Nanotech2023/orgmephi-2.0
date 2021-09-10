import enum
from common import get_current_db

db = get_current_db()


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


class StageConditionEnum(enum.Enum):
    No = "No"
    And = "And"
    Or = "Or"


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

    contests = db.relationship('SimpleContest', secondary=contestsInStage, lazy='subquery',
                               backref=db.backref('stage', lazy=True, uselist=False))


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
                         db.Column('task_id', db.Integer, db.ForeignKey('base_task.task_id'), primary_key=True)
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
