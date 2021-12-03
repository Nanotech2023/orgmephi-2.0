import enum
from datetime import datetime, timedelta

from sqlalchemy import extract, select
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case

from common import get_current_db
from contest.tasks.models import Stage, contestsInStage
from user.models.auth import Group

db = get_current_db()

DEFAULT_VISIBILITY = True

"""
Olympiad level
"""


class OlympiadLevelEnum(enum.Enum):
    Level1 = "1"
    Level2 = "2"
    Level3 = "3"
    Level4 = "No level"


"""
Olympiad status
"""


class OlympiadStatusEnum(enum.Enum):
    OlympiadSoon = "Will start soon"
    OlympiadInProgress = "In progress"
    OlympiadFinished = "Finished"


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
    NaturalSciences = "Natural Sciences"
    EngineeringSciences = "Engineering Sciences"
    Other = "Other"


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
                               backref='olympiad_type')


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
    certificate_type: contest certificate template
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
    level = db.Column(db.Enum(OlympiadLevelEnum), nullable=False)
    certificate_type_id = db.Column(db.Integer, db.ForeignKey('certificate_type.certificate_type_id',
                                                              ondelete='SET NULL'))

    winner_1_condition = db.Column(db.Float, nullable=False)
    winner_2_condition = db.Column(db.Float, nullable=False)
    winner_3_condition = db.Column(db.Float, nullable=False)
    diploma_1_condition = db.Column(db.Float, nullable=False)
    diploma_2_condition = db.Column(db.Float, nullable=False)
    diploma_3_condition = db.Column(db.Float, nullable=False)

    target_classes = db.relationship('TargetClass', secondary=targetClassInContest, lazy='subquery',
                                     backref=db.backref('base_contest', lazy=True))

    child_contests = db.relationship('Contest', lazy='dynamic',
                                     backref='base_contest', cascade="all, delete-orphan")
    task_pools = db.relationship('TaskPool', backref='base_contest', lazy='dynamic')


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
    show_answer_after_contest = db.Column(db.Boolean, nullable=True, default=False)

    visibility = db.Column(db.Boolean, default=DEFAULT_VISIBILITY, nullable=False)

    users = db.relationship('UserInContest', lazy='dynamic',
                            backref='contest')

    group_restrictions = db.relationship('ContestGroupRestriction', lazy='dynamic', cascade="all, delete")
    contest_tasks = db.relationship('ContestTask', backref='contest', lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': ContestTypeEnum.Contest,
        'polymorphic_on': composite_type
    }

    @hybrid_property
    def academic_year(self):
        if self.composite_type == ContestTypeEnum.CompositeContest:
            return CompositeContest.query.filter_by(contest_id=self.contest_id).one_or_none().academic_year
        else:
            return SimpleContest.query.filter_by(contest_id=self.contest_id).one_or_none().academic_year

    @academic_year.expression
    def academic_year(cls):
        return case(
            [
                (
                    cls.composite_type == ContestTypeEnum.CompositeContest,
                    select(CompositeContest.academic_year).where(
                        CompositeContest.contest_id == cls.contest_id
                    ).limit(1).scalar_subquery()
                )
            ],
            else_=select(SimpleContest.academic_year).where(
                SimpleContest.contest_id == cls.contest_id
            ).limit(1).scalar_subquery()
        ).label("academic_year")

    @hybrid_property
    def user_count(self):
        if self.composite_type == ContestTypeEnum.CompositeContest:
            return CompositeContest.query.filter_by(contest_id=self.contest_id).one_or_none().user_count
        else:
            return SimpleContest.query.filter_by(contest_id=self.contest_id).one_or_none().user_count


def add_simple_contest(db_session,
                       visibility,
                       start_date,
                       end_date,
                       regulations=None,
                       result_publication_date=None,
                       show_answer_after_contest=False,
                       end_of_enroll_date=None,
                       deadline_for_appeal=None,
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
        show_answer_after_contest=show_answer_after_contest,
        regulations=regulations,
        holding_type=holding_type,
        contest_duration=contest_duration,
        result_publication_date=result_publication_date,
        end_of_enroll_date=end_of_enroll_date,
        deadline_for_appeal=deadline_for_appeal,
        previous_contest_id=previous_contest_id,
        previous_participation_condition=previous_participation_condition,
    )
    db_session.add(simple_contest)
    from user.models.auth import get_group_for_everyone
    everyone_group: Group = get_group_for_everyone()
    add_group_restriction(db_session, simple_contest.contest_id, everyone_group.id,
                          ContestGroupRestrictionEnum.edit_user_status)
    return simple_contest


class SimpleContest(Contest):
    """
    Simple contest model.

    contest_id: id of contest

    start_date: start date of contest
    end_of_enroll_date: end of enroll date
    deadline_for_appeal: deadline_for_appeal
    end_date: end date of contest
    result_publication_date: result publication date

    regulations: regulations of the olympiad

    location: location of the olympiad
    previous_contest_id: previous contest id
    previous_participation_condition: previous participation condition
    contest_duration: duration of the contest
    variants: variants
    next_contest: next contests

    """
    __tablename__ = 'simple_contest'

    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True)

    start_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    result_publication_date = db.Column(db.DateTime, nullable=True)
    end_of_enroll_date = db.Column(db.DateTime, nullable=True)
    deadline_for_appeal = db.Column(db.DateTime, nullable=True)
    contest_duration = db.Column(db.Interval, default=timedelta(seconds=0), nullable=False)
    target_classes = association_proxy('base_contest', 'target_classes')
    previous_contest_id = db.Column(db.Integer, db.ForeignKey('simple_contest.contest_id'), nullable=True)
    previous_participation_condition = db.Column(db.Enum(UserStatusEnum))

    regulations = db.Column(db.Text, nullable=True)

    variants = db.relationship('Variant', backref='simple_contest', lazy='dynamic')
    next_contests = db.relationship('SimpleContest',
                                    foreign_keys=[previous_contest_id])

    locations = db.relationship('OlympiadLocation', secondary=locationInContest, lazy='subquery',
                                backref=db.backref('contest', lazy=True))

    name = association_proxy('base_contest', 'name')
    subject = association_proxy('base_contest', 'subject')

    __mapper_args__ = {
        'polymorphic_identity': ContestTypeEnum.SimpleContest,
        'with_polymorphic': '*'
    }

    @hybrid_property
    def academic_year(self):
        if self.start_date.month < 9:
            return self.start_date.year - 1
        else:
            return self.start_date.year

    @academic_year.expression
    def academic_year(cls):
        return case(
            [
                (
                    extract('month', cls.start_date) < 9,
                    extract('year', cls.start_date) - 1
                )
            ],
            else_=extract('year', cls.start_date)
        ).label("academic_year")

    def change_previous(self, previous_contest_id=None, previous_participation_condition=None):
        if previous_contest_id is not None:
            self.previous_contest_id = previous_contest_id
        if previous_participation_condition is not None:
            self.previous_participation_condition = previous_participation_condition

    @hybrid_property
    def tasks_number(self):
        if not self.variants:
            return None
        else:
            if self.variants.count() != 0:
                tasks = self.variants.first().contest_tasks_in_variant.all()
                return len(tasks)
            else:
                return None

    @hybrid_property
    def total_points(self):
        if not self.variants:
            return None
        else:
            if self.variants.count() != 0:
                sum_points = 0
                tasks = self.variants.first().contest_tasks_in_variant.all()
                if len(tasks) != 0:
                    for task in tasks:
                        sum_points += task.contest_task.task_points
                    return sum_points
                else:
                    return None
            else:
                return None

    @hybrid_property
    def status(self):
        if datetime.utcnow() < self.start_date:
            return OlympiadStatusEnum.OlympiadSoon
        elif datetime.utcnow() < self.end_date:
            return OlympiadStatusEnum.OlympiadInProgress
        else:
            return OlympiadStatusEnum.OlympiadFinished

    @status.expression
    def status(cls):
        return case([(datetime.utcnow() < cls.start_date, OlympiadStatusEnum.OlympiadSoon.value),
                     (datetime.utcnow() < cls.end_date, OlympiadStatusEnum.OlympiadInProgress.value)],
                    else_=OlympiadStatusEnum.OlympiadFinished.value)

    @hybrid_property
    def user_count(self):
        from contest.tasks.models import UserInContest
        return UserInContest.query.filter_by(contest_id=self.contest_id).count()


def add_group_restriction(db_session, contest_id, group_id, restriction):
    group_restriction = ContestGroupRestriction(
        contest_id=contest_id,
        group_id=group_id,
        restriction=restriction
    )
    db_session.add(group_restriction)


class ContestGroupRestrictionEnum(enum.Enum):
    view_mark_and_user_status = 'ViewMarkAndUserStatus'
    view_response = 'ViewResponse'
    edit_mark = 'EditMark'
    edit_user_status = 'EditUserStatus'


restriction_range = {elem.value: i for i, elem in enumerate(ContestGroupRestrictionEnum)}


class ContestGroupRestriction(db.Model):
    """
    Contest Group Restriction model

    contest_id: id of the contest
    group_id: id of the group
    restriction: restriction for group
    """
    contest_id = db.Column(db.Integer, db.ForeignKey(Contest.contest_id), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id), primary_key=True)
    restriction = db.Column(db.Enum(ContestGroupRestrictionEnum))

    group = db.relationship(Group, uselist=False)
    group_name = association_proxy('group', 'name')


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
                             backref='composite_contest')

    __mapper_args__ = {
        'polymorphic_identity': ContestTypeEnum.CompositeContest,
        'with_polymorphic': '*'
    }

    @hybrid_property
    def academic_year(self):
        if len(self.stages.all()) == 0:
            return None
        stage = self.stages.all()[0]
        if len(stage.contests) == 0:
            return None
        contest = stage.contests[0]
        if contest.start_date.month < 9:
            return contest.start_date.year - 1
        else:
            return contest.start_date.year

    # noinspection PyMethodParameters
    @academic_year.expression
    def academic_year(cls):
        contest_start_date = select(SimpleContest.start_date).where(
            select(contestsInStage.columns.contest_id)
            .where(
                select(Stage.stage_id)
                .where(
                    Stage.olympiad_id == cls.contest_id
                ).limit(1).scalar_subquery() == contestsInStage.columns.stage_id
            ).limit(1).scalar_subquery() == cls.contest_id
        ).scalar_subquery()

        return case(
            [
                (
                    extract('month', contest_start_date) < 9,
                    extract('year', contest_start_date) - 1
                )
            ],
            else_=extract('year', contest_start_date)
        ).label("academic_year")

    @hybrid_property
    def status(self):
        over = 0
        not_started = 0
        for stage in self.stages.all():
            for contest in stage.contests:
                if datetime.utcnow() < contest.start_date:
                    not_started += 1
                elif datetime.utcnow() < contest.end_date:
                    return OlympiadStatusEnum.OlympiadInProgress
                else:
                    over += 1
        if over == 0:
            return OlympiadStatusEnum.OlympiadSoon
        elif not_started == 0:
            return OlympiadStatusEnum.OlympiadFinished
        else:
            return OlympiadStatusEnum.OlympiadInProgress

    @hybrid_property
    def user_count(self):
        from contest.tasks.models import UserInContest
        stages = [stage for stage in self.stages.all()]
        staged_contests = []
        for stage in stages:
            staged_contests.extend([contest_s for contest_s in stage.contests])
        users = [UserInContest.query.filter_by(contest_id=composite_elem.contest_id).count()
                 for composite_elem in staged_contests]
        return sum(users)
