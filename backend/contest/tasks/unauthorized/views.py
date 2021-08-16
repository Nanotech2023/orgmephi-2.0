from flask import make_response

from common import get_current_app, get_current_module
from common.util import db_get_all
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


# Olympiad types


@module.route('/olympiad_type/all', methods=['GET'])
def olympiad_type_all():
    """
    Get all olympiad types
    """
    olympiad_types = db_get_all(OlympiadType)
    all_olympiad_types = [olympiad_type.serialize() for olympiad_type in olympiad_types]
    return make_response(
        {"olympiad_types": all_olympiad_types}, 200)


@module.route('/olympiad_type/<int:id_olympiad_type>', methods=['GET'])
def olympiad_type_get(id_olympiad_type):
    olympiad = db_get_or_raise(OlympiadType, "olympiad_type_id", str(id_olympiad_type))
    return make_response(olympiad.serialize(), 200)


# Olympiad
# TODO Target class checking ???


@module.route('/base_olympiad/all', methods=['GET'])
def base_olympiads_all():
    """
    Get base olympiads list
    """
    olympiads = db_get_all(BaseContest)
    all_olympiads = [olympiad.serialize() for olympiad in olympiads]
    return make_response(
        {"olympiad_list": all_olympiads}, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>', methods=['GET'])
def base_olympiad_get(id_base_olympiad):
    """
    Get base olympiad
    """
    base_contest = db_get_or_raise(BaseContest, "base_contest_id", id_base_olympiad)
    return make_response(base_contest.serialize(), 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/all', methods=['GET'])
def olympiads_all(id_base_olympiad):
    """
    Get olympiads list
    """
    base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
    all_olympiads = [olympiad.serialize() for olympiad in base_contest.child_contests]
    return make_response(
        {"olympiad_list": all_olympiads}, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>', methods=['GET'])
def olympiad_get(id_base_olympiad, id_olympiad):
    """
    Get olympiad
    """
    db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
    contest = db_get_or_raise(Contest, "contest_id", id_olympiad)
    return make_response(contest.serialize(), 200)


# Stage


@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>', methods=['GET'])
def stage_get(id_olympiad, id_stage):
    """
    Get stage
    """
    try:
        olympiad = db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
        if olympiad.composite_type != ContestTypeEnum.CompositeContest or stage not in olympiad.stages:
            raise InsufficientData('stage_id', 'not in current olympiad')
        return make_response(
            stage.serialize(), 200)
    except Exception:
        raise


@module.route('/olympiad/<int:id_olympiad>/stage/all', methods=['GET'])
def stages_all(id_olympiad):
    """
    Get stages list
    """
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    contest = db_get_or_raise(CompositeContest, "contest_id", str(id_olympiad))
    all_stages = [stage.serialize() for stage in contest.stages]
    return make_response(
        {
            "stages_list": all_stages
        }, 200)


# Contest


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/all',
    methods=['GET'])
def contest_all_self(id_olympiad, id_stage):
    """
    Get all contests for user in current stage
    """
    olympiad = db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    if olympiad.composite_type != ContestTypeEnum.CompositeContest or stage not in olympiad.stages:
        raise InsufficientData('stage_id', 'not in current olympiad')
    all_contest = [contest_.serialize()
                   for contest_ in stage.contests
                   if is_user_in_contest(jwt_get_id(), contest_)]
    return make_response(
        {
            "contest_list": all_contest
        }, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>',
    methods=['GET'])
def contest_self(id_olympiad, id_stage, id_contest):
    """
    Get contest for user in current stage
    """
    contest = get_user_contest_if_possible(id_olympiad, id_stage, id_contest)
    return make_response(contest.serialize(), 200)

