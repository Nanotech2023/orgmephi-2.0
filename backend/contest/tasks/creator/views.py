from flask import request, make_response

from common import get_current_app, get_current_module
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/base_olympiad/create', methods=['POST'])
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
def base_olympiad_upload(id_base_olympiad):
    certificate_template = request.data

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
def base_olympiad_remove(id_base_olympiad):
    try:
        base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
        db.session.delete(base_contest)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>', methods=['PATCH'])
def base_olympiad_patch(id_base_olympiad):
    base_contest = db_get_or_raise(BaseContest, "base_contest_id", id_base_olympiad)
    values = request.openapi.body

    try:
        db_get_or_raise(OlympiadType, "olympiad_type_id", values["olympiad_type_id"])
        target_classes = set(values['target_classes'])
        del values["target_classes"]
        base_contest.update(values)
        if target_classes is not None:
            base_contest.target_classes = target_classes

        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response(base_contest.serialize(), 200)


# Olympiads


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/createsimple', methods=['POST'])
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


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/remove', methods=['POST'])
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


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>', methods=['PATCH'])
def olympiad_patch(id_base_olympiad, id_olympiad):
    contest = db_get_or_raise(Contest, "contest_id", id_olympiad)
    values = request.openapi.body

    try:
        db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
        contest.update(values)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return make_response(contest.serialize(), 200)


# Stage views


@module.route('/olympiad/<int:id_olympiad>/stage/create', methods=['POST'])
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
              methods=['PATCH'])
def stage_patch(id_olympiad, id_stage):
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    try:
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        values = request.openapi.body
        stage.update(values)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return make_response(stage.serialize(), 200)


# Contest views
@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/createsimple',
              methods=['POST'])
def contest_create_simple(id_olympiad, id_stage):
    values = request.openapi.body

    visibility = values['visibility']
    start_time = values['start_time']
    end_time = values['end_time']
    location = values.get('location', None)
    previous_contest_id = values.get('previous_contest_id', None)
    previous_participation_condition = values.get('previous_participation_condition', None)

    try:
        validate_contest_values(previous_contest_id, previous_participation_condition)

        stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))

        contest = add_simple_contest(db.session,
                                     visibility=visibility,
                                     start_date=start_time,
                                     end_date=end_time,
                                     previous_contest_id=previous_contest_id,
                                     previous_participation_condition=previous_participation_condition,
                                     location=location)

        stage.contests.append(contest)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            'contest_id': contest.contest_id
        }, 200)


# TODO: WILL IT BE DELETED ?
@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/createcomposite',
              methods=['POST'])
def contest_create_composite(id_olympiad, id_stage):
    values = request.openapi.body

    visibility = values['visibility']

    try:
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        stage = db_get_or_raise(Stage, "stage_id", str(id_stage))

        contest = add_composite_contest(db.session,
                                        visibility=visibility)

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
def contest_remove(id_olympiad, id_stage, id_contest):
    try:
        contest = get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest)
        db.session.delete(contest)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>',
    methods=['GET', 'PATCH'])
def contest_patch(id_olympiad, id_stage, id_contest):
    values = request.openapi.body
    try:
        contest = get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest)
        contest.update(values)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response(contest.serialize(), 200)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/add_previous',
    methods=['PATCH'])
def contest_add_previous(id_olympiad, id_stage, id_contest):
    contest = get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest)
    values = request.openapi.body
    try:
        contest.change_previous(**values)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return make_response({}, 200)


@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/all',
              methods=['GET'])
def contests_all(id_olympiad, id_stage):
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db_get_or_raise(Stage, "stage_id", str(id_stage))
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    all_contests = [contest.serialize() for contest in stage.contests]
    return make_response(
        {"olympiad_list": all_contests}, 200)


# Variant views


@module.route(
    '/contest/<int:id_contest>/variant/create',
    methods=['POST'])
def variant_create(id_contest):
    values = request.openapi.body
    contest = get_contest_if_possible(id_contest)
    last_variant_number = get_last_variant_in_contest(contest)
    variant_description = values['variant_description']

    try:
        variant = add_variant(db.session,
                              variant_number=last_variant_number + 1,
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
    '/contest/<int:id_contest>/variant/<int:id_variant>/remove',
    methods=['POST'])
def variant_remove(id_contest, id_variant):
    try:
        variant = get_variant_if_possible(id_contest, id_variant)

        db.session.delete(variant)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/contest/<int:id_contest>/variant/<int:variant_num>',
    methods=['GET'])
def variant_get(id_contest, variant_num):
    variant = get_variant_if_possible_by_number(id_contest, variant_num)
    return make_response(
        variant.serialize(), 200)


@module.route(
    '/contest/<int:id_contest>/variant/<int:variant_num>',
    methods=['PATCH'])
def variant_patch(id_contest, variant_num):
    values = request.openapi.body
    try:
        variant = get_variant_if_possible_by_number(id_contest, variant_num)
        variant.update(values)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return make_response(variant.serialize(), 200)


@module.route(
    '/contest/<int:id_contest>/variant/all',
    methods=['GET'])
def variant_all(id_contest):
    contest = get_contest_if_possible(id_contest)
    all_variants = [variant.serialize() for variant in contest.variants.all()]
    return make_response(
        {
            "variants_list": all_variants
        }, 200)


# Task views


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/createplain',
    methods=['POST'])
def task_create_plain(id_contest, id_variant):
    values = request.openapi.body

    num_of_task = values['num_of_task']
    image_of_task = values['image_of_task']
    recommended_answer = values['recommended_answer']

    try:
        variant = get_variant_if_possible(id_contest, id_variant)

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
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/createrange',
    methods=['POST'])
def task_create_range(id_contest, id_variant):
    values = request.openapi.body
    num_of_task = values['num_of_task']
    image_of_task = values['image_of_task']
    start_value = values['start_value']
    end_value = values['end_value']

    try:
        variant = get_variant_if_possible(id_contest, id_variant)
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
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/createmultiple',
    methods=['POST'])
def task_create_multiple(id_contest, id_variant):
    values = request.openapi.body

    num_of_task = values['num_of_task']
    image_of_task = values['image_of_task']
    answers = values['answers']
    try:
        variant = get_variant_if_possible(id_contest, id_variant)

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
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/remove',
    methods=['POST'])
def task_remove(id_contest, id_variant, id_task):
    try:
        task = get_task_if_possible(id_contest, id_variant, id_task)
        db.session.delete(task)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>',
    methods=['GET'])
def task_get(id_contest, id_variant, id_task):
    task = get_task_if_possible(id_contest, id_variant, id_task)
    return make_response(
        task.serialize(), 200)


def check_existence(id_olympiad, id_stage, id_contest, id_variant):
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db_get_or_raise(Stage, "stage_id", str(id_stage))
    db_get_or_raise(Contest, "contest_id", str(id_contest))
    db_get_or_raise(Variant, "variant_id", str(id_variant))


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/plain',
    methods=['PATCH'])
def task_patch_plain(id_contest, id_variant, id_task):
    values = request.openapi.body
    try:
        task = get_task_if_possible(id_contest, id_variant, id_task)
        task.update(values)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/range',
    methods=['PATCH'])
def task_patch_range(id_contest, id_variant, id_task):
    values = request.openapi.body
    try:
        task = get_task_if_possible(id_contest, id_variant, id_task)
        task.update(values)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/multiple',
    methods=['PATCH'])
def task_patch_multiple(id_contest, id_variant, id_task):
    values = request.openapi.body
    try:
        task = get_task_if_possible(id_contest, id_variant, id_task)
        answers = values['answers']
        del values['answers']

        task.update(values)

        task.answers = [
            (answer['task_answer'], answer['is_right_answer'])
            for answer in answers]

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/all',
    methods=['GET'])
def task_all(id_contest, id_variant):
    tasks = get_tasks_if_possible(id_contest, id_variant)
    return make_response(
        {
            "tasks_list": tasks
        }, 200)


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/tasks/<int:id_task>/image',
    methods=['GET'])
def task_image(id_contest, id_variant, id_task):
    task = get_task_if_possible(id_contest, id_variant, id_task)

    return make_response(
        task.serialize_image(), 200)
