import enum
from datetime import datetime

from sqlalchemy.ext.associationproxy import association_proxy

from common import get_current_db

db = get_current_db()

DEFAULT_VISIBILITY = True


class UserStatusEnum(enum.Enum):
    """
    Enum for user statuses
    """
    Winner_1 = "Winner 1"
    Winner_2 = "Winner 2"
    Winner_3 = "Winner 3"
    Diploma_1 = "Diploma 1"
    Diploma_2 = "Diploma 2"
    Diploma_3 = "Diploma 3"
    Participant = "Participant"


user_status_weights_dict = {
    status[1].value: len(UserStatusEnum) - status[0]
    for status
    in enumerate(UserStatusEnum)
}


class OlympiadSubjectEnum(enum.Enum):
    """
    Enum for olympiad subject
    """
    Math = "Math"
    Physics = "Physics"
    Informatics = "Informatics"


olympiad_subject_dict = {subject.value: subject for subject in OlympiadSubjectEnum}


def add_olympiad_type(olympiad_type):
    """
    Create new olympiad type object
    """
    olympiad = OlympiadType(
        olympiad_type=olympiad_type,
    )
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


def add_base_contest(db_session, name,
                     winner_1_condition,
                     winner_2_condition,
                     winner_3_condition,
                     diploma_1_condition,
                     diploma_2_condition,
                     diploma_3_condition,
                     description, rules,
                     olympiad_type_id,
                     subject,
                     certificate_template):
    """
    Create new base content object
    """
    base_contest = BaseContest(
        description=description,
        name=name,
        certificate_template=certificate_template,
        rules=rules,
        winner_1_condition=winner_1_condition,
        winner_2_condition=winner_2_condition,
        winner_3_condition=winner_3_condition,
        diploma_1_condition=diploma_1_condition,
        diploma_2_condition=diploma_2_condition,
        diploma_3_condition=diploma_3_condition,
        olympiad_type_id=olympiad_type_id,
        subject=subject
    )
    db_session.add(base_contest)
    return base_contest


# Contest models


targetClassInContest = db.Table('target_classes_in_contest',
                                db.Column('base_contest_id', db.Integer,
                                          db.ForeignKey('base_contest.base_contest_id'),
                                          primary_key=True),
                                db.Column('target_class_id', db.Integer,
                                          db.ForeignKey('target_class.target_class_id'),
                                          primary_key=True)
                                )


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
    conditions: Diploma 3, Diploma 2, Diploma 1, Winner 3, Winner 2, Winner 1
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

    winner_1_condition = db.Column(db.Float, nullable=False)
    winner_2_condition = db.Column(db.Float, nullable=False)
    winner_3_condition = db.Column(db.Float, nullable=False)
    diploma_1_condition = db.Column(db.Float, nullable=False)
    diploma_2_condition = db.Column(db.Float, nullable=False)
    diploma_3_condition = db.Column(db.Float, nullable=False)

    target_classes = db.relationship('TargetClass', secondary=targetClassInContest, lazy='subquery',
                                     backref=db.backref('base_contest', lazy=True))

    child_contests = db.relationship('Contest', lazy='dynamic',
                                     backref=db.backref('base_contest', lazy='joined'), cascade="all, delete-orphan")


class ContestTypeEnum(enum.Enum):
    Contest = "Contest"
    SimpleContest = "SimpleContest"
    CompositeContest = "CompositeContest"


class ContestHoldingTypeEnum(enum.Enum):
    OfflineContest = "OfflineContest"
    OnLineContest = "OnLineContest"


locationInContest = db.Table('location_in_contest',
                             db.Column('contest_id', db.Integer, db.ForeignKey('contest.contest_id'),
                                       primary_key=True),
                             db.Column('location_id', db.Integer, db.ForeignKey('olympiad_location.location_id'),
                                       primary_key=True)
                             )


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
    holding_type = db.Column(db.Enum(ContestHoldingTypeEnum))

    visibility = db.Column(db.Boolean, default=DEFAULT_VISIBILITY, nullable=False)

    users = db.relationship('UserInContest', lazy='dynamic',
                            backref=db.backref('contest', lazy='joined'))

    __mapper_args__ = {
        'polymorphic_identity': ContestTypeEnum.Contest,
        'polymorphic_on': composite_type,
        'with_polymorphic': '*'
    }


def add_simple_contest(db_session,
                       visibility,
                       start_date,
                       end_date,
                       result_publication_date=None,
                       end_of_enroll_date=None,
                       holding_type=None,
                       contest_duration=None,
                       previous_contest_id=None,
                       previous_participation_condition=None,
                       base_contest_id=None):
    """
    Create new simple contest object
    """
    simple_contest = SimpleContest(
        base_contest_id=base_contest_id,
        visibility=visibility,
        start_date=start_date,
        end_date=end_date,
        holding_type=holding_type,
        contest_duration=contest_duration,
        result_publication_date=result_publication_date,
        end_of_enroll_date=end_of_enroll_date,
        previous_contest_id=previous_contest_id,
        previous_participation_condition=previous_participation_condition,
    )
    db_session.add(simple_contest)
    return simple_contest


class SimpleContest(Contest):
    """
    Simple contest model.

    contest_id: id of contest

    start_date: start date of contest
    end_of_enroll_date: end of enroll date
    end_date: end date of contest
    result_publication_date: result publication date

    location: location of the olympiad
    previous_contest_id: previous contest id
    previous_participation_condition: previous participation condition
    contest_duration: previous duration of the contest
    variants: variants
    next_contest: next contests

    """
    __tablename__ = 'simple_contest'

    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True)

    start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    result_publication_date = db.Column(db.DateTime, nullable=True)
    end_of_enroll_date = db.Column(db.DateTime, nullable=True)

    contest_duration = db.Column(db.Interval, nullable=True)

    target_classes = association_proxy('base_contest', 'target_classes')

    previous_contest_id = db.Column(db.Integer, db.ForeignKey('simple_contest.contest_id'), nullable=True)
    previous_participation_condition = db.Column(db.Enum(UserStatusEnum))

    variants = db.relationship('Variant', lazy='dynamic',
                               backref=db.backref('simple_contest', lazy='joined'))

    next_contests = db.relationship('SimpleContest',
                                    foreign_keys=[previous_contest_id])

    locations = db.relationship('OlympiadLocation', secondary=locationInContest, lazy='subquery',
                                backref=db.backref('contest', lazy=True))

    __mapper_args__ = {
        'polymorphic_identity': ContestTypeEnum.SimpleContest,
        'with_polymorphic': '*'
    }

    def change_previous(self, previous_contest_id=None, previous_participation_condition=None):
        if previous_contest_id is not None:
            self.previous_contest_id = previous_contest_id
        if previous_participation_condition is not None:
            self.previous_participation_condition = previous_participation_condition


def add_composite_contest(db_session, visibility, base_contest_id=None, holding_type=None):
    """
    Create new composite contest object
    """
    composite_contest = CompositeContest(
        base_contest_id=base_contest_id,
        holding_type=holding_type,
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

    stages = db.relationship('Stage', lazy='dynamic',
                             backref=db.backref('composite_contest', lazy='joined'))

    __mapper_args__ = {
        'polymorphic_identity': ContestTypeEnum.CompositeContest,
        'with_polymorphic': '*'
    }
