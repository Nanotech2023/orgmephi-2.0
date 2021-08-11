import random

from flask import abort
from flask import request, make_response

from common import get_current_module
from common.jwt_verify import jwt_required_role
from common.errors import NotFound, AlreadyExists, InsufficientData
from common.util import db_get_all, db_get_one_or_none
from .models import *

db = get_current_db()
module = get_current_module()


# Olympiad types


@module.route('/olympiad_type/create', methods=['POST'])
@jwt_required_role(['Admin'])
def olympiad_type_create():
    values = request.openapi.body

    olympiad_type = values['olympiad_type']

    try:
        type_of_olympiad = db_get_one_or_none(OlympiadType, "olympiad_type", str(olympiad_type))
        if type_of_olympiad is not None:
            raise AlreadyExists('olympiad_type', olympiad_type)
        olympiad = add_olympiad_type(db.session,
                                     olympiad_type=olympiad_type)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            'olympiad_type_id': olympiad.olympiad_type_id
        }, 200)


@module.route('/olympiad_type/<int:id_olympiad_type>/remove', methods=['POST'])
@jwt_required_role(['Admin'])
def olympiad_type_remove(id_olympiad_type):
    try:
        olympiad = db_get_or_raise(OlympiadType, "olympiad_type_id", str(id_olympiad_type))
        db.session.delete(olympiad)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route('/olympiad_type/<int:id_olympiad_type>', methods=['GET'])
def olympiad_type_get(id_olympiad_type):
    olympiad = db_get_or_raise(OlympiadType, "olympiad_type_id", str(id_olympiad_type))
    return make_response(olympiad.serialize(), 200)


@module.route('/olympiad_type/all', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def olympiad_type_all():
    olympiad_types = db_get_all(OlympiadType)
    all_olympiad_types = [olympiad_type.serialize() for olympiad_type in olympiad_types]
    return make_response(
        {"olympiad_types": all_olympiad_types}, 200)


# Olympiad views

@module.route('/base_olympiad/create', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_create():
    values = request.openapi.body

    name = values['name']
    description = values['description']
    rules = values['rules']
    olympiad_type_id = values['olympiad_type_id']
    winning_condition = values['winning_condition']
    laureate_condition = values['laureate_condition']
    subject = values['subject']
    target_classes = set(values['target_classes'])

    try:
        db_get_or_raise(OlympiadType, "olympiad_type_id", values["olympiad_type_id"])
        base_contest = add_base_contest(db.session,
                                        description=description,
                                        name=name,
                                        certificate_template=None,
                                        winning_condition=winning_condition,
                                        laureate_condition=laureate_condition,
                                        rules=rules,
                                        olympiad_type_id=olympiad_type_id,
                                        subject=subject)

        base_contest.target_classes = target_classes

        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            'base_contest_id': base_contest.base_contest_id
        }, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/upload_certificate', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_upload(id_base_olympiad):
    certificate_template = request.files['certificate_template'].stream.read()

    try:
        base_contest = db_get_or_raise(BaseContest, "base_contest_id", id_base_olympiad)
        base_contest.certificate_template = certificate_template
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {}, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/remove', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_remove(id_base_olympiad):
    try:
        base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
        db.session.delete(base_contest)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def base_olympiad_get(id_base_olympiad):
    base_contest = db_get_or_raise(BaseContest, "base_contest_id", id_base_olympiad)

    return make_response(base_contest.serialize(), 200)


@module.route('/base_olympiad/<int:id_base_olympiad>', methods=['PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_patch(id_base_olympiad):
    base_contest = db_get_or_raise(BaseContest, "base_contest_id", id_base_olympiad)
    values = request.openapi.body

    try:
        db_get_or_raise(OlympiadType, "olympiad_type_id", values["olympiad_type_id"])
        target_classes = set(values['target_classes'])
        del values["target_classes"]
        base_contest.update(**values)
        if target_classes is not None:
            base_contest.target_classes = target_classes

        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response(base_contest.serialize(), 200)


@module.route('/base_olympiad/all', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def base_olympiads_all():
    olympiads = db_get_all(BaseContest)
    all_olympiads = [olympiad.serialize() for olympiad in olympiads]
    return make_response(
        {"olympiad_list": all_olympiads}, 200)


# Olympiads

@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/createsimple', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def olympiad_create_simple(id_base_olympiad):
    values = request.openapi.body

    visibility = values['visibility']
    start_time = values['start_time']
    end_time = values['end_time']
    previous_contest_id = values.get('previous_contest_id', None)
    location = values.get('location', None)
    previous_participation_condition = values.get('previous_participation_condition', None)

    try:
        base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
        contest = add_simple_contest(db.session,
                                     visibility=visibility,
                                     start_date=start_time,
                                     end_date=end_time,
                                     previous_participation_condition=previous_participation_condition,
                                     location=location,
                                     )
        if previous_contest_id is not None:
            prev_contest = db_get_or_raise(Contest, "contest_id", str(previous_contest_id))
            prev_contest.next_contests.append(contest)
        base_contest.child_contests.append(contest)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            'contest_id': contest.contest_id
        }, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/createcomposite', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def olympiad_create_composite(id_base_olympiad):
    values = request.openapi.body

    visibility = values['visibility']

    try:
        base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
        contest = add_composite_contest(db.session,
                                        visibility=visibility)
        base_contest.child_contests.append(contest)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            'contest_id': contest.contest_id
        }, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/all', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def olympiads_all(id_base_olympiad):
    base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
    all_olympiads = [olympiad.serialize() for olympiad in base_contest.child_contests]
    return make_response(
        {"olympiad_list": all_olympiads}, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/remove', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def olympiad_remove(id_base_olympiad, id_olympiad):
    try:
        db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
        contest = db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        db.session.delete(contest)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def olympiad_get(id_base_olympiad, id_olympiad):
    db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
    contest = db_get_or_raise(Contest, "contest_id", id_olympiad)
    return make_response(contest.serialize(), 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>', methods=['PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def olympiad_patch(id_base_olympiad, id_olympiad):
    contest = db_get_or_raise(Contest, "contest_id", id_olympiad)
    values = request.openapi.body

    try:
        db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
        contest.update(**values)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return make_response(contest.serialize(), 200)


# Stage views

@module.route('/olympiad/<int:id_olympiad>/stage/create', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def stage_create(id_olympiad):
    values = request.openapi.body
    stage_name = values['stage_name']
    stage_num = values['stage_num']
    condition = values['condition']
    this_stage_condition = values['this_stage_condition']

    try:
        contest = db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        if contest.composite_type == ContestTypeEnum.SimpleContest:
            raise InsufficientData('contest.composite_type', 'not composite')
        stage = add_stage(db.session,
                          stage_name=stage_name,
                          stage_num=stage_num,
                          condition=condition,
                          this_stage_condition=this_stage_condition,
                          )
        contest.stages.append(stage)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return make_response(
        {
            'stage_id': stage.stage_id
        }, 200)


@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>/remove',
              methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def stage_remove(id_olympiad, id_stage):
    try:
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
        db.session.delete(stage)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>',
              methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def stage_get(id_olympiad, id_stage):
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))

    return make_response(
        stage.serialize(), 200)


@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>',
              methods=['PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def stage_patch(id_olympiad, id_stage):
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    try:
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        values = request.openapi.body
        stage.update(**values)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return make_response(stage.serialize(), 200)


@module.route('/olympiad/<int:id_olympiad>/stage/all', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def stages_all(id_olympiad):
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    contest = db_get_or_raise(CompositeContest, "contest_id", str(id_olympiad))
    all_stages = [stage.serialize() for stage in contest.stages]
    return make_response(
        {
            "stages_list": all_stages
        }, 200)


# Contest views
@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest'
              '/createsimple',
              methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contest_create_simple(id_olympiad, id_stage):
    values = request.openapi.body

    visibility = values['visibility']
    start_time = values['start_time']
    end_time = values['end_time']
    location = values.get('location', None)
    previous_contest_id = values.get('previous_contest_id', None)
    previous_participation_condition = values.get('previous_participation_condition', None)

    try:
        if (previous_participation_condition is None and previous_contest_id is not None) or \
                (previous_participation_condition is not None and previous_contest_id is None):
            raise InsufficientData("previous contest", "id or condition")
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        contest = add_simple_contest(db.session,
                                     visibility=visibility,
                                     start_date=start_time,
                                     end_date=end_time,
                                     previous_contest_id=previous_contest_id,
                                     previous_participation_condition=previous_participation_condition,
                                     location=location)

        stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
        stage.contests.append(contest)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            'contest_id': contest.contest_id
        }, 200)


@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest'
              '/createcomposite',
              methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contest_create_composite(id_olympiad, id_stage):
    values = request.openapi.body

    visibility = values['visibility']

    try:
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        contest = add_composite_contest(db.session,
                                        visibility=visibility)

        stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
        stage.contests.append(contest)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            'contest_id': contest.contest_id
        }, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/remove',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contest_remove(id_olympiad, id_stage, id_contest):
    try:
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        db_get_or_raise(Stage, "stage_id", str(id_stage))
        contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
        db.session.delete(contest)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>',
    methods=['GET', 'PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contest_response(id_olympiad, id_stage, id_contest):
    contest = db_get_or_raise(Contest, "contest_id", id_contest)
    if request.method == 'GET':
        try:
            db_get_or_raise(Contest, "contest_id", str(id_olympiad))
            stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
            if contest not in stage.contests:
                raise InsufficientData('contest_id', 'not in current stage')
            return make_response(contest.serialize(), 200)
        except Exception:
            raise

    if request.method == 'PATCH':
        values = request.openapi.body

        try:
            db_get_or_raise(Contest, "contest_id", str(id_olympiad))
            stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
            if contest not in stage.contests:
                raise InsufficientData('contest_id', 'not in current stage')
            contest.update(**values)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return make_response(contest.serialize(), 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/'
    '<int:id_contest>/addprevious',
    methods=['PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contest_add_previous(id_olympiad, id_stage, id_contest):
    contest = db_get_or_raise(Contest, "contest_id", id_contest)
    values = request.openapi.body
    try:
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        db_get_or_raise(Stage, "stage_id", str(id_stage))
        contest.change_previous(**values)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return make_response({}, 200)


@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/all',
              methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contests_all(id_olympiad, id_stage):
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db_get_or_raise(Stage, "stage_id", str(id_stage))
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    all_contests = [contest.serialize() for contest in stage.contests]
    return make_response(
        {"olympiad_list": all_contests}, 200)


# Variant views


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/create',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def variant_create(id_olympiad, id_stage, id_contest):
    values = request.openapi.body

    contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    variants = contest.variants.all()
    if len(variants) > 0:
        new_variant = max(variant.variant_number for variant in variants)
    else:
        new_variant = 0

    variant_description = values['variant_description']

    try:
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        db_get_or_raise(Stage, "stage_id", str(id_stage))
        contest = db_get_or_raise(Contest, "contest_id", str(id_contest))

        variant = add_variant(db.session,
                              variant_number=new_variant + 1,
                              variant_description=variant_description,
                              )
        contest.variants.append(variant)

        db.session.add(variant)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            "variant_id": variant.variant_id,
        }, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/remove',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def variant_remove(id_olympiad, id_stage, id_contest, id_variant):
    try:
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        db_get_or_raise(Stage, "stage_id", str(id_stage))
        contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
        variant = contest.variants.filter_by(**{"variant_id": str(id_variant)}).one_or_none()

        db.session.delete(variant)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:variant_num>',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def variant_get(id_olympiad, id_stage, id_contest, variant_num):
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db_get_or_raise(Stage, "stage_id", str(id_stage))
    contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    variant = contest.variants.filter_by(**{"variant_number": str(variant_num)}).one_or_none()

    if variant is None:
        raise NotFound("variant_number", str(variant_num))

    return make_response(
        variant.serialize(), 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:variant_num>',
    methods=['PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def variant_patch(id_olympiad, id_stage, id_contest, variant_num):
    try:
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        db_get_or_raise(Stage, "stage_id", str(id_stage))
        contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
        variant = contest.variants.filter_by(**{"variant_number": str(variant_num)}).one_or_none()

        values = request.openapi.body
        variant.update(**values)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return make_response(variant.serialize(), 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/all',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def variant_all(id_olympiad, id_stage, id_contest):
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db_get_or_raise(Stage, "stage_id", str(id_stage))
    contest = db_get_or_raise(Contest, "contest_id", id_contest)
    all_variants = [variant.serialize() for variant in contest.variants.all()]
    return make_response(
        {
            "variants_list": all_variants
        }, 200)


# Task views


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/createplain',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_create_plain(id_olympiad, id_stage, id_contest, id_variant):
    try:
        check_existence(id_olympiad, id_stage, id_contest, id_variant)
        variant = db_get_or_raise(Variant, "variant_id", str(id_variant))
        values = request.openapi.body

        num_of_task = values['num_of_task']
        image_of_task = values['image_of_task']

        recommended_answer = values['recommended_answer']

        task = add_plain_task(db.session,
                              num_of_task=num_of_task,
                              image_of_task=image_of_task,
                              recommended_answer=recommended_answer,
                              )

        variant.tasks.append(task)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            "task_id": task.task_id,
        }, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/createrange',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_create_range(id_olympiad, id_stage, id_contest, id_variant):
    try:
        check_existence(id_olympiad, id_stage, id_contest, id_variant)
        variant = db_get_or_raise(Variant, "variant_id", str(id_variant))

        values = request.openapi.body

        num_of_task = values['num_of_task']
        image_of_task = values['image_of_task']

        start_value = values['start_value']
        end_value = values['end_value']

        task = add_range_task(db.session,
                              num_of_task=num_of_task,
                              image_of_task=image_of_task,
                              start_value=start_value,
                              end_value=end_value
                              )
        variant.tasks.append(task)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            "task_id": task.task_id,
        }, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/createmultiple',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_create_multiple(id_olympiad, id_stage, id_contest, id_variant):
    try:
        check_existence(id_olympiad, id_stage, id_contest, id_variant)
        variant = db_get_or_raise(Variant, "variant_id", str(id_variant))

        values = request.openapi.body

        num_of_task = values['num_of_task']
        image_of_task = values['image_of_task']

        answers = values['answers']

        task = add_multiple_task(db.session,
                                 num_of_task=num_of_task,
                                 image_of_task=image_of_task
                                 )
        variant.tasks.append(task)

        task.answers = [
            (answer['task_answer'], answer['is_right_answer'])
            for answer in answers]

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return make_response(
        {
            "task_id": task.task_id,
        }, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/<int:id_task>/remove',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_remove(id_olympiad, id_stage, id_contest, id_variant, id_task):
    try:
        check_existence(id_olympiad, id_stage, id_contest, id_variant)
        task = db_get_or_raise(Task, "task_id", str(id_task))
        db.session.delete(task)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/<int:id_task>',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def task_get(id_olympiad, id_stage, id_contest, id_variant, id_task):
    check_existence(id_olympiad, id_stage, id_contest, id_variant)
    task = db_get_or_raise(Task, "task_id", str(id_task))

    return make_response(
        task.serialize(), 200)


def check_existence(id_olympiad, id_stage, id_contest, id_variant):
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db_get_or_raise(Stage, "stage_id", str(id_stage))
    db_get_or_raise(Contest, "contest_id", str(id_contest))
    db_get_or_raise(Variant, "variant_id", str(id_variant))


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/<int:id_task>/plain',
    methods=['PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_patch_plain(id_olympiad, id_stage, id_contest, id_variant, id_task):
    try:
        check_existence(id_olympiad, id_stage, id_contest, id_variant)

        task = db_get_or_raise(PlainTask, "task_id", str(id_task))
        values = request.openapi.body
        task.update(**values)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/<int:id_task>/range',
    methods=['PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_patch_range(id_olympiad, id_stage, id_contest, id_variant, id_task):
    try:
        task = db_get_or_raise(RangeTask, "task_id", str(id_task))
        check_existence(id_olympiad, id_stage, id_contest, id_variant)
        values = request.openapi.body
        task.update(**values)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/<int:id_task>/multiple',
    methods=['PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_patch_multiple(id_olympiad, id_stage, id_contest, id_variant, id_task):
    try:
        check_existence(id_olympiad, id_stage, id_contest, id_variant)
        task = db_get_or_raise(MultipleChoiceTask, "task_id", str(id_task))
        values = request.openapi.body
        answers = values['answers']
        del values['answers']
        task.update(**values)

        task.answers = [
            (answer['task_answer'], answer['is_right_answer'])
            for answer in answers]

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/all',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_all(id_olympiad, id_stage, id_contest, id_variant):
    check_existence(id_olympiad, id_stage, id_contest, id_variant)
    variant = db_get_or_raise(Variant, "variant_id", str(id_variant))
    all_tasks = [task.serialize() for task in variant.tasks]
    return make_response(
        {
            "tasks_list": all_tasks
        }, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/tasks/<int:id_task>/taskimage',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_image(id_olympiad, id_stage, id_contest, id_variant, id_task):
    check_existence(id_olympiad, id_stage, id_contest, id_variant)
    task = db_get_or_raise(Task, "task_id", str(id_task))

    return make_response(
        {
            "task_id": task.task_id,
            "image_of_task": task.image_of_task
        }, 200)


# User views

def generate_variant(id_contest, user_id):
    contest = db_get_or_raise(Contest, "contest_id", id_contest)
    variants_number = len(contest.variants.all())
    if variants_number == 0:
        raise InsufficientData('variant', 'variants in contest')
    random_number = random.randint(0, variants_number * 2)
    variant = (user_id + random_number) % variants_number
    return variant


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/adduser',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def add_user_to_contest(id_olympiad, id_stage, id_contest):
    values = request.openapi.body
    user_ids = values['users_id']
    try:
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        db_get_or_raise(Stage, "stage_id", str(id_stage))
        contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
        for user_id in user_ids:
            if contest.users.filter_by(**{"user_id": str(user_id)}).one_or_none() is not None:
                raise AlreadyExists('user_id', user_id)
            add_user_in_contest(db.session,
                                user_id=user_id,
                                contest_id=id_contest,
                                variant_id=generate_variant(id_contest, user_id),
                                user_status=UserStatusEnum.Participant
                                )

        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {}, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/removeuser',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def remove_user_from_contest(id_olympiad, id_stage, id_contest):
    values = request.openapi.body
    user_ids = values['users_id']

    try:
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        db_get_or_raise(Stage, "stage_id", str(id_stage))
        contest = db_get_or_raise(Contest, "contest_id", str(id_contest))

        for user_id in user_ids:
            user = contest.users.filter_by(**{"user_id": str(user_id)}).one_or_none()
            db.session.delete(user)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/user/all',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def users_all(id_olympiad, id_stage, id_contest):
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db_get_or_raise(Stage, "stage_id", str(id_stage))
    db_get_or_raise(Contest, "contest_id", str(id_contest))
    contest = db_get_or_raise(Contest, "contest_id", id_contest)
    all_users = [u.serialize() for u in contest.users.all()]
    return make_response(
        {
            "user_list": all_users
        }, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>'
    '/user/<int:id_user>/certificate',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def users_certificate(id_olympiad, id_stage, id_contest, id_user):
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db_get_or_raise(Stage, "stage_id", str(id_stage))
    contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    contest.users.filter_by(**{"user_id": str(id_user)}).one_or_none()
    # contest = db_get_or_raise(Contest, Contest.contest_id, id_contest)
    # user = db_get_or_raise(UserInContest, UserInContest.user_id, id_user)

    # certificate = None

    abort(502)

    """return make_response(
            {
                "certificate": certificate
            }, 200)"""
