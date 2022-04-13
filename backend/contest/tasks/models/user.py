from common import get_current_db
from contest.tasks.models import UserStatusEnum
from user.models import User

db = get_current_db()


class UserInContest(db.Model):
    """
    Class describing a User in contest model.

    user_id: if of user
    contest_id: id of the contest
    supervisor: supervisor of the olympiad
    variant_id: variant connected with current contest
    user_status: user status: laureate, winner or custom value
    show_results_to_user: can user see his results
    completed_the_contest: hsd user completed his contest
    """

    __tablename__ = 'user_in_contest'

    user_id = db.Column(db.Integer, db.ForeignKey(f'{User.__table_name__}.id'), primary_key=True)
    proctoring_login = db.Column(db.String, default=None, nullable=True)
    proctoring_password = db.Column(db.String, default=None, nullable=True)
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'), primary_key=True)
    variant_id = db.Column(db.Integer, db.ForeignKey('variant.variant_id'))
    user_status = db.Column(db.Enum(UserStatusEnum))
    supervisor = db.Column(db.Text, nullable=True)
    show_results_to_user = db.Column(db.Boolean)
    completed_the_contest = db.Column(db.Boolean, default=False)
    location_id = db.Column(db.Integer, db.ForeignKey('olympiad_location.location_id'))


class ExternalContestResult(db.Model):
    """
    Class describing contest result on other platform

    work_id: id of work
    user_id: id of user
    contest_id: id of the contest
    num_of_task: number of the tusk
    task_points: number of points for task
    """

    __tablename__ = 'external_contest_results'

    work_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(f'{User.__table_name__}.id'))
    contest_id = db.Column(db.Integer, db.ForeignKey('contest.contest_id'))
    num_of_task = db.Column(db.Integer)
    task_points = db.Column(db.Integer)
