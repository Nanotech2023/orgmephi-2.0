from flask import abort, request, make_response

from common import get_current_app, get_current_module
from common.errors import AlreadyExists
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


# Users


@module.route(
    '/contest/<int:id_contest>/add_user',
    methods=['POST'])
def add_user_to_contest(id_contest):
    """
    Add user to contest
    """
    values = request.openapi.body
    user_ids = values['users_id']
    try:
        contest = get_contest_if_possible(id_contest)

        for user_id in user_ids:
            if is_user_in_contest(user_id, contest):
                raise AlreadyExists('user_id', user_id)

            contest.users.append(UserInContest(user_id=user_id,
                                               variant_id=generate_variant(id_contest, user_id),
                                               user_status=UserStatusEnum.Participant))

        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {}, 200)


@module.route(
    '/contest/<int:id_contest>/remove_user',
    methods=['POST'])
def remove_user_from_contest(id_olympiad, id_stage, id_contest):
    """
    Remove user from contest
    """
    values = request.openapi.body
    user_ids = values['users_id']

    try:
        contest = get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest)

        for user_id in user_ids:
            user = contest.users.filter_by(**{"user_id": str(user_id)}).one_or_none()
            db.session.delete(user)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/contest/<int:id_contest>/user/all',
    methods=['GET'])
def users_all(id_olympiad, id_stage, id_contest):
    """
    Get all user in contest
    """
    contest = get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest)
    all_users = [u.serialize() for u in contest.users.all()]
    return make_response(
        {
            "user_list": all_users
        }, 200)


@module.route(
    'contest/<int:id_contest>/user/<int:id_user>/certificate',
    methods=['GET'])
def users_certificate(id_olympiad, id_stage, id_contest, id_user):
    """
    Get user certificate
    """
    # contest = get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest)
    # certificate = None

    abort(502)
