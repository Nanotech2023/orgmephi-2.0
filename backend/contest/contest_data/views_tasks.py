import datetime

from flask import request, make_response, abort, send_file
import re
from os import getcwd

import sqlalchemy.exc

from common.errors import RequestError, NotFound, InsufficientData
from common import get_current_app, get_current_module
from common.jwt_verify import jwt_required, jwt_required_role, jwt_get_id

db = get_current_db()
module = get_current_module()
app = get_current_app()

#TODO
# - move user to another stage
# - open contest for user
# - check everything linked with api
# - check everything linked with model


def catch_request_error(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except RequestError as err:
            return err.to_response()

    return wrapper


def get_or_raise(entity, field, value):
    result = get_one_or_null(entity, field, value)
    if result is None:
        raise NotFound(field, value)
    return result


def get_missing(values, search):
    missing = []
    for value in search:
        if value not in values:
            missing.append(value)
    return missing


# Swagger UI

@module.route('/tasks_api.yaml', methods=['GET'])
def get_api():
    if app.config['ENV'] != 'development':
        abort(404)
    api_path = app.config['ORGMEPHI_API_PATH']
    if api_path[0] != '/':
        api_path = '%s/%s' % (getcwd(), api_path)
    return send_file(api_path)


# Olympiad views

@module.route('/base_olympiad/create', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_create():
    values = request.openapi.body

    name = values['name']
    description = values['description']
    rules = values['rules']
    olympiad_type = values['olympiad_type']
    certificate_template = values['certificate_template']
    subject = values['subject']
    target_classes = values['target_classes']

    try:
        baseContest = add_base_contest(db.session,
                                       description=description,
                                       name=name,
                                       certificate_template=certificate_template,
                                       rules=rules,
                                       olympiad_type=olympiad_type,
                                       subject=subject)

        for target_class in target_classes:
            target_class = add_target_class(db.session,
                                            contest_id=contest.contest_id,
                                            target_class=olympiad_target_class_dict[target_class],
                                            )

        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response(baseContest.serialize(), 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/remove', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_remove(id_base_olympiad):
    try:
        baseContest = get_or_raise(BaseContest, BaseContest.base_contest_id, id_base_olympiad)
        db.session.delete(baseContest)
        db.session.commit()
        return make_response({}, 200)
    except Exception:
        db.session.rollback()
        raise


@module.route('/base_olympiad/<int:id_base_olympiad>', methods=['GET', 'PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_response(id_base_olympiad):
    baseContest = get_or_raise(BaseContest, BaseContest.base_contest_id, id_base_olympiad)

    if request.method == 'GET':
        return make_response(baseContest.serialize(), 200)

    elif request.method == 'PATCH':
        values = request.openapi.body

        try:
            base_olympiad.update(**values)
            target_classes = values["target_classes"]
            if target_classes is not None:
                update_target_class(db.session, id_base_olympiad, target_classes)
        except Exception:
            db.session.rollback()
            raise
        db.session.commit()
        return make_response(base_olympiad.serialize(), 200)


@module.route('/base_olympiad/all', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiads_all():
    try:
        olympiads = get_all(Olympiad)
        all_olympiads = [olympiad.serialize() for olympiad in olympiads]

        return make_response(
            {"olympiad_list": all_olympiads}, 200)
    except Exception:
        db.session.rollback()
        raise


# Olympiads

@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/create', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def olympiad_create(id_base_olympiad):
    values = request.openapi.body

    composite_type = values['composite_type']
    base_contest_id = values['base_contest_id']
    winning_condition = values['winning_condition']
    laureate_condition = values['laureate_condition']
    visibility = values['visibility']

    try:

        if composite_type == "Composite":

            start_date = values['start_date']
            end_date = values['end_date']
            previous_contest_id = values['previous_contest_id']
            previous_participation_condition = values['previous_participation_condition']

            contest = add_simple_contest(db.session,
                                         base_contest_id,
                                         winning_condition,
                                         laureate_condition,
                                         visibility,
                                         start_date,
                                         end_date,
                                         previous_contest_id,
                                         previous_participation_condition)


        else:
            contest = add_composite_contest(db_session,
                                            base_contest_id,
                                            winning_condition,
                                            laureate_condition,
                                            certificate_template,
                                            visibility)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(contest.serialize(), 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/remove', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_remove(id_base_olympiad, id_olympiad):
    try:
        contest = get_or_raise(Contest, Contest.contest_id, id_olympiad)
        db.session.delete(contest)
        db.session.commit()
        return make_response({}, 200)
    except Exception:
        db.session.rollback()
        raise


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>', methods=['GET', 'PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_response(id_base_olympiad, id_olympiad):
    contest = get_or_raise(Contest, Contest.contest_id, id_olympiad)

    if request.method == 'GET':
        if contest.composite_type == CompositeTypeEnum.Composite:
            contest = get_or_raise(SimpleContest, SimpleContest.contest_id, id_olympiad)
            return make_response(contest.serialize(), 200)
        else:
            contest = get_or_raise(CompositeContest, CompositeContest.contest_id, id_olympiad)
            return make_response(contest.serialize(), 200)

    elif request.method == 'PATCH':
        values = request.openapi.body

        try:
            contest.update(**values)
        except Exception:
            db.session.rollback()
            raise

        db.session.commit()

        return make_response(base_olympiad.serialize(), 200)


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

    return make_response(stage.serialize(), 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/remove',
              methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def stage_remove(id_base_olympiad, id_olympiad, id_stage):
    try:
        stage = get_or_raise(Stage, Stage.stage_id, id_stage)
        db.session.delete(stage)
        db.session.commit()
        return make_response({}, 200)
    except Exception:
        db.session.rollback()
        raise


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>',
              methods=['GET', 'PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def stage_response(id_base_olympiad, id_olympiad, id_stage):
    stage = get_or_raise(Stage, Stage.stage_id, id_stage)
    if request.method == 'GET':
        try:
            return make_response(
                {
                    stage.serialize()
                }, 200)

        except Exception:
            db.session.rollback()
            raise
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

        contest = get_or_raise(CompositeContest, CompositeContest.contest_id, id_olympiad)
        stages = Stage.query.all()
        all_stages = [stage.serialize() for stage in stages]

        return make_response(
            {
                "stages_list": all_stages
            }, 200)

    except Exception:
        db.session.rollback()
        raise


# Contest views

@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/create',
              methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contest_create(id_base_olympiad, id_olympiad, id_stage):
    values = request.openapi.body

    composite_type = values['composite_type']
    base_contest_id = values['base_contest_id']
    winning_condition = values['winning_condition']
    laureate_condition = values['laureate_condition']
    visibility = values['visibility']
    location = values['location']

    try:

        if composite_type == "Composite":

            start_date = values['start_date']
            end_date = values['end_date']
            previous_contest_id = values['previous_contest_id']
            previous_participation_condition = values['previous_participation_condition']

            contest = add_simple_contest(db.session,
                                         base_contest_id,
                                         winning_condition,
                                         laureate_condition,
                                         visibility,
                                         start_date,
                                         end_date,
                                         previous_contest_id,
                                         previous_participation_condition)


        else:
            contest = add_composite_contest(db_session,
                                            base_contest_id,
                                            winning_condition,
                                            laureate_condition,
                                            certificate_template,
                                            visibility)

        contestsInStageObject = add_contest_in_stage(db.session,
                                                     stage_id=id_stage,
                                                     contest_id=contest.contest_id,
                                                     location=location,
                                                     )



        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return make_response(contest.serialize(), 200)


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/remove',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contest_remove(id_base_olympiad, id_olympiad, id_stage, id_contest):
    try:
        contest = get_or_raise(Contest, Contest.contest_id, id_olympiad)
        db.session.delete(contest)
        db.session.commit()
        return make_response({}, 200)

    except Exception:
        db.session.rollback()
        raise


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>',
    methods=['GET','PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contest_response(id_base_olympiad, id_olympiad, id_stage, id_contest):
    contest = get_or_raise(Contest, Contest.contest_id, id_olympiad)
    if request.method == 'GET':
        try:
            return make_response(contest.serialize(), 200)

        except Exception:
            db.session.rollback()
            raise

    if request.method == 'PATCH':
        values = request.openapi.body

        try:
            contest.update(**values)
        except Exception:
            db.session.rollback()
            raise

        db.session.commit()

        return make_response(base_olympiad.serialize(), 200)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/all',
              methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def contests_all(id_base_olympiad, id_olympiad, id_stage):
    contest_ids = contestsInStage.query.filter_by(contestsInStage.stage_id == id_stage).all()

    all_contests = []
    for contest_id in contest_ids:
        contest = get_or_raise(Contest, Contest.contest_id, contest_id)
        all_contests.append(contest)

    return make_response(
        {"olympiad_list": all_contests}, 200)


# Variant views


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/variant/create',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def variant_create(id_base_olympiad, id_olympiad, id_stage, id_contest):
    values = request.openapi.body

    contest = get_or_raise(Contest, Contest.contest_id, id_contest)
    contest.variants.all()

    variant_description = values['variant_description']

    try:
        variant = add_variant(db.session,
                              contest_id=id_contest,
                              variant_number=len(contest) + 1,
                              variant_description=variant_description,
                              )

        db.session.add(variant)

        db.session.commit()
        return make_response(
            {
                "variant_id": variant.variant_id,
            }, 200)

    except Exception:
        db.session.rollback()
        raise


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/variant/<int:id_variant>/remove',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def variant_remove(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant):
    try:
        variant = get_or_raise(Variant, Variant.variant_id, id_variant)
        db.session.delete(variant)
        db.session.commit()
        return make_response({}, 200)
    except Exception:
        db.session.rollback()
        raise


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/variant/<int:variant_num>',
    methods=['GET', 'PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def variant_get(id_base_olympiad, id_olympiad, id_stage, id_contest, variant_num):
    variant = get_or_raise(Variant, Variant.variant_id, id_variant)
    if request.method == 'GET':
        try:
            return make_response(
                {
                    variant.serialize()
                }, 200)

        except Exception:
            db.session.rollback()
            raise
    elif request.method == 'PATCH':
        try:
            values = request.openapi.body
            variant.update(**values)
            db.session.commit()
            return make_response(variant.serialize(), 200)

        except Exception:
            db.session.rollback()
            raise


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/variant/all',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def variant_all(id_base_olympiad, id_olympiad, id_stage, id_contest):
    try:
        variants = get_all(Variant)
        all_variants = [variant.serialize() for variant in variants]

        return make_response(
            {
                "variants_list": all_variants
            }, 200)
    except Exception:
        db.session.rollback()
        raise


# Task views


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/variant/<int:id_variant>/task/create',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_create(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant):
    try:
        task = None
        values = request.openapi.body

        num_of_task = values['num_of_task']
        image_of_task = values['image_of_task']

        if 'recommended_answer' in values:
            recommended_answer = values['image_of_task']

            task = add_plain_task(
                num_of_task=num_of_task,
                image_of_task=image_of_task,
                type=TaskType.plain_task,
            )

        elif 'start_value' in values:
            start_value = values['start_value']
            end_value = values['end_value']

            task = add_range_task(
                num_of_task=num_of_task,
                image_of_task=image_of_task,
                type=type,
                start_value=start_value,
                end_value=end_value
            )

        else:
            answers = values['answers']

            task = add_multiple_task(
                num_of_task=num_of_task,
                image_of_task=image_of_task,
                type=type
            )

            for answer in answers:
                answerForTask = add_answer_to_multiple_task(
                    task_id=task.task_id,
                    answer=answer['answer'],
                    correct=answer['is_right_answer'],
                )

        db.session.commit()
        return make_response(
            {
                "task_id": task.task_id,
            }, 200)

    except Exception:
        db.session.rollback()
        raise


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/remove',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_remove(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant, id_task):
    try:
        task = Task.query.filter_by(Task.task_id == id_task).one()

        if task.type == TaskType.plain_task:
            plainTask = PlainTask.query.filter_by(PlainTask.task_id == id_task).one()
            db.session.delete(plainTask)

        if task.type == TaskType.range_task:
            rangeTask = RangeTask.query.filter_by(RangeTask.task_id == id_task).one()
            db.session.delete(rangeTask)

        if task.type == TaskType.multiple_task:
            multipleTask = MultipleTask.query.filter_by(MultipleTask.task_id == id_task).one()

            for answer in multipleTask.all_answers_in_multiple_task.all():
                db.session.delete(answer)

            db.session.delete(multipleTask)

        db.session.commit()
        return make_response({}, 200)

    except Exception:
        db.session.rollback()
        raise


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>',
    methods=['GET', 'PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_get(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant, id_task):
    if request.method == 'GET':
        try:
            task = Task.query.filter_by(Task.task_id == id_task).one()

            if task.type == TaskType.plain_task:
                plainTask = PlainTask.query.filter_by(PlainTask.task_id == id_task).one()

                return make_response(
                    {
                        plainTask.serialize()
                    }, 200)

            elif task.type == TaskType.range_task:
                rangeTask = RangeTask.query.filter_by(RangeTask.task_id == id_task).one()

                return make_response(
                    {
                        rangeTask.serialize()
                    }, 200)

            elif task.type == TaskType.multiple_task:
                multipleTask = MultipleTask.query.filter_by(MultipleTask.task_id == id_task).one()

                return make_response(
                    {
                        multipleTask.serialize()
                    }, 200)

        except Exception:
            db.session.rollback()
            raise

    elif request.method == 'PATCH':
        try:
            task = Task.query.filter_by(Task.task_id == id_task).one()

            values = request.openapi.body

            if task.type == TaskType.plain_task:
                plainTask = get_or_raise(PlainTask, PlainTask.task_id, id_task)
                plainTask.update(**values)

            elif task.type == TaskType.range_task:
                rangeTask = get_or_raise(RangeTask, RangeTask.task_id, id_task)
                rangeTask.update(**values)

            elif task.type == TaskType.multiple_task:
                multipleTask = get_or_raise(MultipleTask, MultipleTask.task_id, id_task)
                multipleTask.update(**values)
                answers = values['answers']
                updateMultipleChoiceTask(db.session, task_id, answers)

            db.session.commit()
            return make_response({}, 200)

        except Exception:
            db.session.rollback()
            raise



@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/variant/<int:id_variant>/task/all',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_all(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant):
    try:
        variant = get_or_raise(Variant, Variant.id_variant, id_variant)
        all_tasks = [task.serialize() for task in variant.tasks]

        return make_response(
            {
                "tasks_list": all_tasks
            }, 200)

    except Exception:
        db.session.rollback()
        raise


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/taskimage',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def task_image(id_base_olympiad, id_olympiad, id_stage, id_contest, id_variant, id_task):
    try:
        tasks = get_or_raise(Task, Task.task_id, id_task)

        return make_response(
            {
                "task_id": task.task_id,
                "image_of_task": task.image_of_task
            }, 200)

    except Exception:
        db.session.rollback()
        raise


# User views

@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/adduser',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def add_user_to_contest(id_base_olympiad, id_olympiad, id_stage, id_contest):
    values = request.openapi.body
    user_ids = values['users_id']

    try:

        for user_id in user_ids:
            user = add_user_in_contest(
                user_id=user_id,
                contest_id=id_contest,
                variant_id=None,  # TODO HOW TO CHOOSE VARIANT
                user_status= UserStatusEnum.Participant

            )

        db.session.commit()
        return make_response(
            {
                "users_id": user_ids,
            }, 200)

    except Exception:
        db.session.rollback()
        raise


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/{id_contest}/removeuser:',
    methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def remove_user_from_contest(id_base_olympiad, id_olympiad, id_stage, id_contest):
    values = request.openapi.body
    user_ids = values['users_id']

    try:
        for user_id in user_ids:
            user = get_or_raise(UserInContest, UserInContest.user_id, user_id)
            db.session.delete(user)

        db.session.commit()
        return make_response({}, 200)

    except Exception:
        db.session.rollback()
        raise


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/{id_contest}/user/all',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def users_all(id_base_olympiad, id_olympiad, id_stage, id_contest):
    try:
        users = get_all(UserInContest)

        all_users = []

        for user in users:
            all_users.append(
                {
                    user.serialize()
                }
            )

        return make_response(
            {
                "user_list": all_users
            }, 200)

    except Exception:
        db.session.rollback()
        raise


@module.route(
    '/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/{id_contest}/user/<int:id_user>/certificate',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def users_all(id_base_olympiad, id_olympiad, id_stage, id_contest, id_user):
    try:
        contest = get_or_raise(Contest, Contest.contest_id, id_contest)
        user = get_or_raise(UserInContest, UserInContest.user_id, id_user)

        certificate = getCertificateFromTemplate(user, contest.certificate_template) #TODO Function to generate it

        return make_response(
            {
                "certificate": certificate
            }, 200)

    except Exception:
        db.session.rollback()
        raise

