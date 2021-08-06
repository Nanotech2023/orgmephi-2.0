import random

from flask import abort
from flask import request, make_response
from sqlalchemy import func, desc

from common import get_current_module
from common.jwt_verify import jwt_required_role
from common.util import db_get_all, db_get_or_raise, db_get_list
from common.errors import RequestError
from .models import *

db = get_current_db()
module = get_current_module()


# Olympiad views

@module.route('/base_olympiad/create', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_create():
    values = request.openapi.body

    name = values['name']
    description = values['description']
    rules = values['rules']
    olympiad_type = values['olympiad_type']

    # TODO CORRECT BINARY EXAMPLE

    if 'certificate_template' not in values:
        certificate_template = None
    else:
        certificate_template = values['certificate_template']
    winning_condition = values['winning_condition']
    laureate_condition = values['laureate_condition']
    subject = values['subject']
    target_classes = values['target_classes']

    try:
        baseContest = add_base_contest(db.session,
                                       description=description,
                                       name=name,
                                       certificate_template=certificate_template,
                                       winning_condition=winning_condition,
                                       laureate_condition=laureate_condition,
                                       rules=rules,
                                       olympiad_type=olympiad_type,
                                       subject=subject)

        for target_class in target_classes:
            baseContest.target_classes.append(TargetClass(
                target_class=olympiad_target_class_dict[target_class],
            ))

        db.session.commit()
    except RequestError as req:
        req.to_response()
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            'base_contest_id': baseContest.base_contest_id
        }
        , 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/remove', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_remove(id_base_olympiad):
    try:
        target_classes = db_get_list(TargetClass, "contest_id", id_base_olympiad)
        for target_class in target_classes:
            db.session.delete(target_class)
        baseContest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
        db.session.delete(baseContest)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>', methods=['GET', 'PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_response(id_base_olympiad):
    baseContest = db_get_or_raise(BaseContest, "base_contest_id", id_base_olympiad)

    if request.method == 'GET':
        return make_response(baseContest.serialize(), 200)

    elif request.method == 'PATCH':
        values = request.openapi.body

        try:
            target_classes = values["target_classes"]
            del values["target_classes"]
            baseContest.update(**values)
            if target_classes is not None:
                update_target_class(db.session, id_base_olympiad, target_classes)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return make_response(baseContest.serialize(), 200)


@module.route('/base_olympiad/all', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiads_all():
    try:
        olympiads = db_get_all(BaseContest)
        all_olympiads = [olympiad.serialize() for olympiad in olympiads]
    except Exception:
        raise
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
        contest = add_simple_contest(db.session,
                                     id_base_olympiad,
                                     visibility,
                                     start_time,
                                     end_time,
                                     previous_contest_id,
                                     previous_participation_condition,
                                     location)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            'contest_id': contest.contest_id
        }
        , 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/createcomposite', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def olympiad_create_composite(id_base_olympiad):
    values = request.openapi.body

    visibility = values['visibility']

    try:
        contest = add_composite_contest(db.session,
                                        id_base_olympiad,
                                        visibility)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            'contest_id': contest.contest_id
        }
        , 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/all', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def olympiads_all(id_base_olympiad):
    base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
    all_olympiads = [olympiad.serialize() for olympiad in base_contest.child_contests]
    return make_response(
        {"olympiad_list": all_olympiads}, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/remove', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def olympiad_remove(id_base_olympiad, id_olympiad):
    try:
        contest = db_get_or_raise(Contest, "contest_id", str(id_olympiad))
        db.session.delete(contest)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>', methods=['GET', 'PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def olympiad_response(id_base_olympiad, id_olympiad):
    contest = db_get_or_raise(Contest, "contest_id", id_olympiad)

    if request.method == 'GET':
        return make_response(contest.serialize(), 200)

    elif request.method == 'PATCH':
        values = request.openapi.body

        try:
            contest.update(**values)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        return make_response(contest.serialize(), 200)


# Stage views

@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/create', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def stage_create(id_base_olympiad, id_olympiad):
    values = request.openapi.body
    stage_name = values['stage_name']
    next_stage_condition = values['next_stage_condition']

    try:
        stage = add_stage(db.session,
                          olympiad_id=id_olympiad,
                          stage_name=stage_name,
                          next_stage_condition=next_stage_condition,
                          )
        db.session.add(stage)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return make_response(
        {
            'stage_id': stage.stage_id
        }
        , 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/remove',
              methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def stage_remove(id_base_olympiad, id_olympiad, id_stage):
    try:
        stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
        db.session.delete(stage)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>',
              methods=['GET', 'PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def stage_response(id_base_olympiad, id_olympiad, id_stage):
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))

    if request.method == 'GET':
        return make_response(
            stage.serialize()
            , 200)

    elif request.method == 'PATCH':
        try:
            values = request.openapi.body
            stage.update(**values)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return make_response(stage.serialize(), 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/all', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def stages_all(id_base_olympiad, id_olympiad):
    try:

        contest = db_get_or_raise(CompositeContest, "contest_id", str(id_olympiad))
        all_stages = [stage.serialize() for stage in contest.stages]

    except Exception:
        raise

    return make_response(
        {
            "stages_list": all_stages
        }, 200)


# Contest views
@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest'
              '/createsimple',
              methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contest_create_simple(id_base_olympiad, id_olympiad, id_stage):
    values = request.openapi.body

    visibility = values['visibility']
    start_time = values['start_time']
    end_time = values['end_time']
    location = values.get('location', None)
    previous_contest_id = values.get('previous_contest_id', None)
    previous_participation_condition = values.get('previous_participation_condition', None)

    try:
        contest = add_simple_contest(db.session,
                                     id_base_olympiad,
                                     visibility,
                                     start_time,
                                     end_time,
                                     previous_contest_id,
                                     previous_participation_condition,
                                     location)

        stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
        stage.contests.append(contest)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            'contest_id': contest.contest_id
        }
        , 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest'
              '/createcomposite',
              methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contest_create_composite(id_base_olympiad, id_olympiad, id_stage):
    values = request.openapi.body

    visibility = values['visibility']

    try:
        contest = add_composite_contest(db.session,
                                        id_base_olympiad,
                                        visibility)

        stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
        stage.contests.append(contest)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            'contest_id': contest.contest_id
        }
        , 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/remove',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contest_remove(id_base_olympiad, id_olympiad, id_stage, id_contest):
    try:
        contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
        db.session.delete(contest)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>',
    methods=['GET', 'PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contest_response(id_base_olympiad, id_olympiad, id_stage, id_contest):
    contest = db_get_or_raise(Contest, "contest_id", id_contest)
    if request.method == 'GET':
        return make_response(contest.serialize(), 200)

    if request.method == 'PATCH':
        values = request.openapi.body

        try:
            contest.update(**values)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return make_response(contest.serialize(), 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/all',
              methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contests_all(id_base_olympiad, id_olympiad, id_stage):
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    all_contests = [contest.serialize() for contest in stage.contests]
    return make_response(
        {"olympiad_list": all_contests}, 200)


# Variant views


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/create',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def variant_create(id_base_olympiad, id_olympiad, id_stage, id_contest):
    values = request.openapi.body

    # TODO QUERY FOR MAX
    contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    variants = contest.variants
    new_variant = 0
    for var in variants:
        if var.variant_number > new_variant:
            new_variant = var.variant_number

    variant_description = values['variant_description']

    try:
        variant = add_variant(db.session,
                              contest_id=id_contest,
                              variant_number=new_variant + 1,
                              variant_description=variant_description,
                              )

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
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/remove',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def variant_remove(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant):
    try:
        variant = db_get_or_raise(Variant, "variant_id", str(id_variant))
        db.session.delete(variant)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:variant_num>',
    methods=['GET', 'PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def variant_response(id_base_olympiad, id_olympiad, id_stage, id_contest, variant_num):
    variant = db_get_or_raise(Variant, "variant_number", variant_num)
    if request.method == 'GET':
        return make_response(
            variant.serialize()
            , 200)
    elif request.method == 'PATCH':
        try:
            values = request.openapi.body
            variant.update(**values)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        return make_response(variant.serialize(), 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/all',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def variant_all(id_base_olympiad, id_olympiad, id_stage, id_contest):
    contest = db_get_or_raise(Contest, "contest_id", id_contest)
    all_variants = [variant.serialize() for variant in contest.variants]
    return make_response(
        {
            "variants_list": all_variants
        }, 200)


# Task views


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/createplain',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_create_plain(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant):
    try:
        values = request.openapi.body

        variant = db_get_or_raise(Variant, "variant_id", str(id_variant))

        num_of_task = values['num_of_task']
        image_of_task = values['image_of_task']

        recommended_answer = values['recommended_answer']

        task = add_plain_task(db.session,
                              num_of_task=num_of_task,
                              image_of_task=image_of_task,
                              recommended_answer=recommended_answer,
                              )

        add_task_in_Variant(id_variant, task.task_id)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            "task_id": task.task_id,
        }, 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/createrange',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_create_range(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant):
    try:
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
        add_task_in_Variant(id_variant, task.task_id)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            "task_id": task.task_id,
        }, 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/createmultiple',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_create_multiple(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant):
    try:
        values = request.openapi.body

        num_of_task = values['num_of_task']
        image_of_task = values['image_of_task']

        answers = values['answers']

        task = add_multiple_task(db.session,
                                 num_of_task=num_of_task,
                                 image_of_task=image_of_task
                                 )
        add_task_in_Variant(id_variant, task.task_id)
        for answer in answers:
            task.all_answers_in_multiple_task.append(AnswersInMultipleChoiceTask(answer=answer['task_answer'],
                                                                                 correct=answer['is_right_answer']))

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

    return make_response(
        {
            "task_id": task.task_id,
        }, 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/<int:id_task>/remove',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_remove(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant, id_task):
    try:
        task = db_get_or_raise(Task, "task_id", str(id_task))

        if task.task_type == MultipleChoiceTask.__name__:
            for answer in task.all_answers_in_multiple_task:
                db.session.delete(answer)

        db.session.delete(task)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/<int:id_task>',
    methods=['GET', 'PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_get(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant, id_task):
    task = db_get_or_raise(Task, "task_id", str(id_task))
    if request.method == 'GET':
        return make_response(
            {
                task.serialize()
            }, 200)

    elif request.method == 'PATCH':
        try:

            values = request.openapi.body
            task.update(**values)

            if task.task_type == MultipleChoiceTask.__name__:
                answers = values['answers']
                updateMultipleChoiceTask(db.session, id_task, answers)

            db.session.commit()

        except Exception:
            db.session.rollback()
            raise
    return make_response({}, 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/task/all',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_all(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant):
    variant = db_get_or_raise(Variant, "variant_id", str(id_variant))
    all_tasks = [task.serialize() for task in variant.tasks]

    return make_response(
        {
            "tasks_list": all_tasks
        }, 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:id_variant>/tasks/<int:id_task>/taskimage',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_image(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant, id_task):
    task = db_get_or_raise(Task, "task_id", str(id_task))

    return make_response(
        {
            "task_id": task.task_id,
            "image_of_task": task.image_of_task
        }, 200)


# User views

def generate_variant(id_contest, user_id):
    contest = db_get_or_raise(Contest, "contest_id", id_contest)
    variants_number = len(contest.variants)
    random_number = random.randint(0, variants_number * 2)
    variant = (user_id + random_number) % variants_number
    return variant


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/adduser',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def add_user_to_contest(id_base_olympiad, id_olympiad, id_stage, id_contest):
    values = request.openapi.body
    user_ids = values['users_id']

    try:

        for user_id in user_ids:
            user = add_user_in_contest(db.session,
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
        {
            "users_id": user_ids,
        }, 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/removeuser',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def remove_user_from_contest(id_base_olympiad, id_olympiad, id_stage, id_contest):
    values = request.openapi.body
    user_ids = values['users_id']

    try:
        contest = db_get_or_raise(Contest, "contest_id", id_contest)

        for user_id in user_ids:
            user = UserInContest.query.filter_by(**{"contest_id": id_contest,
                                                    "user_id": user_id}).one_or_none()
            db.session.delete(user)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<'
    'id_contest>/moveusercustom',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def move_user(id_base_olympiad, id_olympiad, id_stage, id_contest):
    values = request.openapi.body
    user_ids = values['users_id']
    next_contest_id = values['next_contest_id']

    try:
        for user_id in user_ids:
            add_user_in_contest(db.session,
                                user_id=user_id,
                                contest_id=next_contest_id,
                                variant_id=generate_variant(id_contest, user_id),
                                user_status=UserStatusEnum.Participant
                                )

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({"users_id": user_ids}, 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<'
    'id_contest>/moveallpossibleusers',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def move_all_user(id_base_olympiad, id_olympiad, id_stage, id_contest):
    contest = db_get_or_raise(Contest, "contest_id", id_contest)
    users = contest.users

    values = request.openapi.body
    next_contest_id = values['next_contest_id']
    user_ids = []
    new_contest = db_get_or_raise(Contest, "previous_contest_id", id_contest)
    moving_condition = new_contest.previous_participation_condition

    try:
        for user in users:
            if user_status_dict[user.user_status] >= moving_condition:
                user_ids.append(user.user_id)
                new_contest.users.append(UserInContest(user_id=user.user_id,
                                                       contest_id=next_contest_id,
                                                       variant_id=generate_variant(id_contest, user.user_id),
                                                       user_status=UserStatusEnum.Participant))
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response({"users_id": user_ids}, 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/user/all',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def users_all(id_base_olympiad, id_olympiad, id_stage, id_contest):
    contest = db_get_or_raise(Contest, "contest_id", id_contest)
    all_users = [u.serialize() for u in contest.users]

    return make_response(
        {
            "user_list": all_users
        }, 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>'
    '/user/<int:id_user>/certificate',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def users_certificate(id_base_olympiad, id_olympiad, id_stage, id_contest, id_user):
    try:
        # contest = db_get_or_raise(Contest, Contest.contest_id, id_contest)
        # user = db_get_or_raise(UserInContest, UserInContest.user_id, id_user)

        # certificate = None

        abort(502)

        """return make_response(
            {
                "certificate": certificate
            }, 200)"""

    except Exception:
        raise
