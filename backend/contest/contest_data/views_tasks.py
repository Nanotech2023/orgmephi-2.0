import datetime

from flask import request, make_response, abort, send_file
import re
from os import getcwd

from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies,\
    get_csrf_token, jwt_required, unset_jwt_cookies


from contest_data.models_task import *
from contest_data.errors import *
from jwt_verify import *
from contest_data import app, db, openapi


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

@app.route('/tasks_api.yaml', methods=['GET'])
def get_api():
    if app.config['ENV'] != 'development':
        abort(404)
    api_path = app.config['ORGMEPHI_API_PATH']
    if api_path[0] != '/':
        api_path = '%s/%s' % (getcwd(), api_path)
    return send_file(api_path)


# Olympiad views

@app.route('/base_olympiad/create', methods=['POST'])
@openapi
@catch_request_error
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_create():
    values = request.openapi.body

    name = values['name']
    description = values['description']
    rules = values['rules']
    olympiad_type = values['olympiad_type']
    subject = values['subject']

    try:
        baseContest = add_base_contest(db.session,
                         name,
                         description,
                         rules,
                         olympiad_type,
                         subject)

        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise AlreadyExists('username', username)
    except Exception:
        db.session.rollback()
        raise
    return make_response(baseContest.serialize(), 200)


@app.route('/base_olympiad/<id_base_olympiad>', methods=['GET'])
@openapi
@catch_request_error
@jwt_required()
def base_olympiad_get(id_base_olympiad):
    baseContest = get_or_raise(BaseContest, BaseContest.base_contest_id, id_base_olympiad)
    return make_response(baseContest.serialize(), 200)



@app.route('/base_olympiad/<id_base_olympiad>', methods=['PATCH'])
@openapi
@catch_request_error
@jwt_required_role(['Admin', 'System', 'Creator'])
def base_olympiad_update(id_base_olympiad):
    base_olympiad = get_or_raise(BaseContest, BaseContest.base_contest_id, id_base_olympiad)
    values = request.openapi.body

    try:
        base_olympiad.update(**values)
    except Exception:
        db.session.rollback()
        raise
    db.session.commit()
    return make_response(base_olympiad.serialize(), 200)


@app.route('/base_olympiad/all', methods=['GET'])
@openapi
@catch_request_error
@jwt_required()
def base_olympiads_all():
    olympiads = get_all(Olympiad)
    all_olympiads = [olympiad.serialize() for olympiad in olympiads]

    return make_response(
        { "olympiad_list": all_olympiads }, 200)


@app.route('/base_olympiad/<base_olympiad_id>/olympiad/create', methods=['POST'])
@openapi
@catch_request_error
@jwt_required_role(['Admin', 'System', 'Creator'])
def olympiad_create():
    values = request.openapi.body

    composite_type = values['composite_type']
    base_contest_id = values['base_contest_id']
    winning_condition = values['winning_condition']
    laureate_condition = values['laureate_condition']
    visibility = values['visibility']
    start_date = values['start_date']

    try:

        if composite_type == "Composite":

            end_date = values['end_date']
            previous_contest_id = values['previous_contest_id']
            previous_participation_condition = values['previous_participation_condition']

            add_simple_contest(db.session,
                               base_contest_id,
                               winning_condition,
                               laureate_condition,
                               visibility,
                               start_date,
                               end_date,
                               previous_contest_id,
                               previous_participation_condition)


        else:

            base_contest_id = values['base_contest_id']
            winning_condition = values['winning_condition']
            laureate_condition = values['laureate_condition']
            visibility = values['visibility']
            start_date = values['start_date']
            end_date = values['end_date']
            previous_contest_id = values['previous_contest_id']
            previous_participation_condition = values['previous_participation_condition']

            add_composite_contest(db_session,
                                  base_contest_id,
                                  winning_condition,
                                  laureate_condition,
                                  certificate_template,
                                  visibility)

        db.session.commit()
        return make_response(
            {
                "olympiad_id": olympiad.olympiad_id,
            }, 200)
    except sqlalchemy.exc.IntegrityError:
        raise AlreadyExists('username', username)
    except Exception:
        db.session.rollback()
        raise
    return make_response(baseContest.serialize(), 200)


"""
@app.route('/olympiad/<id_olympiad>/remove', methods=['POST'])
@openapi
def olympiad_remove(id_olympiad):
    try:
        olympiad = Olympiad.query.filter_by(Olympiad.olympiad_id == id_olympiad).one()
        db.session.delete(olympiad)
        db.session.commit()
        return make_response({}, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>', methods=['GET'])
@openapi
def olympiad_get(id_olympiad):
    try:
        olympiad = Olympiad.query.filter_by(Olympiad.olympiad_id == id_olympiad).one()
        return make_response(
            {
                "olympiad_id": olympiad.olympiad_id,
                "name": olympiad.name,
                "description": olympiad.description,
                "rules": olympiad.rules,
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>', methods=['PATCH'])
@openapi
def olympiad_update(id_olympiad):
    try:
        olympiad = Olympiad.query.filter_by(Olympiad.olympiad_id == id_olympiad).one()

        values = request.openapi.body
        if 'name' in values:
            olympiad.name = values['name']
        if 'description' in values:
            olympiad.description = values['description']
        if 'rules' in values:
            olympiad.rules = values['rules']

        db.session.commit()
        return make_response({}, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/all', methods=['GET'])
@openapi
def olympiads_all():
    try:
        olympiads = Olympiad.query.all()

        all_olympiads = []

        for olympiad in olympiads:
            all_olympiads.append(
                {
                    "olympiad_id": olympiad.id,
                    "name": olympiad.name,
                    "description": olympiad.description,
                    "rules": olympiad.rules,
                }
            )

        return make_response(
            {
                "olympiad_list": all_olympiads
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()
"""

# Stage views

@app.route('/olympiad/<id_olympiad>/stage/create', methods=['POST'])
@openapi
def stage_create(id_olympiad):
    try:
        values = request.openapi.body
        stage_name = values['stage_name']
        next_stage_condition = values['next_stage_condition']

        # TODO Checking

        stage = Stage(
            olympiad_id=id_olympiad,
            stage_name=stage_name,
            next_stage_condition=next_stage_condition,
        )
        db.session.add(stage)

        db.session.commit()
        return make_response(
            {
                "stage_id": stage.stage_id,
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/remove', methods=['POST'])
@openapi
def stage_remove(id_olympiad, id_stage):
    try:
        stage = Stage.query.filter_by(Stage.stage_id == id_stage).one()
        db.session.delete(stage)
        db.session.commit()
        return make_response({}, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>', methods=['GET'])
@openapi
def stage_get(id_olympiad, id_stage):
    try:
        stage = Stage.query.filter_by(Stage.stage_id == id_stage).one()
        return make_response(
            {
                "stage_id": stage.stage_id,
                "stage_name": stage.stage_name,
                "next_stage_condition": stage.next_stage_condition,
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>', methods=['PATCH'])
@openapi
def stage_update(id_olympiad, id_stage):
    try:
        stage = Stage.query.filter_by(Stage.stage_id == id_stage).one()

        values = request.openapi.body
        if 'stage_name' in values:
            stage.stage_name = values['stage_name']
        if 'description' in values:
            stage.next_stage_condition = values['next_stage_condition']

        db.session.commit()

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/all', methods=['GET'])
@openapi
def stages_all(id_olympiad):
    try:
        stages = Stage.query.all()

        all_stages = []

        for stage in stages:
            all_stages.append(
                {
                    "stage_id": stage.stage_id,
                    "stage_name": stage.stage_name,
                    "next_stage_condition": stage.next_stage_condition,
                }
            )

        return make_response(
            {
                "stages_list": all_stages
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


# Contest views


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/create', methods=['POST'])
@openapi
def contest_create(id_olympiad, id_stage):
    try:
        values = request.openapi.body
        description = values['description']
        rules = values['rules']
        winning_condition = values['winning_condition']
        laureate_condition = values['laureate_condition']
        certificate_template = values['certificate_template']
        visibility = values['visibility']
        start_date = values['start_date']
        end_time = values['end_time']

        final_composite_type = CompositeTypeDict[values['composite_type']]

        final_olympiad_type = OlympiadTypeEnum[values['olympiad_type']]

        final_subject = OlympiadSubjectDict[values['subject']]

        final_target_class = []
        for val in values['target_class']:
            final_target_class.append(TargetClassDict[val])


        # TODO Checking

        contest = Contest(
            description=description,
            rules=rules,
            winning_condition=winning_condition,
            laureate_condition=laureate_condition,
            certificate_template=certificate_template,
            visibility=visibility,
            start_date=start_date,
            end_time=end_time,
            composite_type=final_composite_type,
            olympiad_type=final_olympiad_type,
            subject=final_subject,
            target_class=final_target_class,
        )
        db.session.add(contest)

        if final_composite_type == CompositeTypeEnum.Composite:
            db.session.flush()
            contestsInStage_val = contestsInStage(
                stage_id = id_stage,
                contest_id = contest.contest_id,
                location = values['location']
            )
            db.session.add(contestsInStage_val)


        db.session.commit()
        return make_response(
            {
                "contest_id": contest.contest_id,
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/remove', methods=['POST'])
@openapi
def contest_remove(id_olympiad, id_stage, id_contest):
    try:
        contest = Contest.query.filter_by(Contest.contest_id == id_contest).one()
        db.session.delete(contest)
        db.session.commit()
        return make_response({}, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>', methods=['GET'])
@openapi
def contest_get(id_olympiad, id_stage, id_contest):
    try:
        contest = Contest.query.filter_by(Contest.contest_id == id_contest).one()
        return make_response(
            {
                "contest_id": contest.contest_id,
                "description": contest.description,
                "rules": contest.rules,
                "winning_condition": contest.winning_condition,
                "laureate_condition": contest.laureate_condition,
                "certificate_template": contest.certificate_template,
                "visibility": contest.visibility,
                "start_date": contest.start_date,
                "end_time": contest.end_time,
                "composite_type": contest.composite_type,
                "olympiad_type": contest.olympiad_type,
                "subject": contest.subject,
                "target_class": contest.target_class,
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>', methods=['PATCH'])
@openapi
def contest_update(id_olympiad, id_stage, id_contest):
    try:
        contest = Contest.query.filter_by(Contest.contest_id == id_contest).one()

        values = request.openapi.body
        if 'description' in values:
            contest.description = values['description']
        if 'rules' in values:
            contest.rules = values['rules']
        if 'winning_condition' in values:
            contest.winning_condition = values['winning_condition']
        if 'laureate_condition' in values:
            contest.laureate_condition = values['laureate_condition']
        if 'certificate_template' in values:
            contest.certificate_template = values['description']
        if 'description' in values:
            contest.description = values['description']
        if 'start_date' in values:
            contest.start_date = values['start_date']
        if 'end_time' in values:
            contest.end_time = values['end_time']

        if 'composite_type' in values:
            contest.composite_type = CompositeTypeDict[values['composite_type']]

        if 'olympiad_type' in values:
            contest.olympiad_type = OlympiadTypeEnum[values['olympiad_type']]

        if 'subject' in values:
            contest.subject = OlympiadSubjectDict[values['subject']]

        if 'target_class' in values:
            contest.target_class = []
            for val in values['target_class']:
                contest.target_class.append(TargetClassDict[val])

        db.session.commit()
        return make_response({}, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/all', methods=['GET'])
@openapi
def contests_all(id_olympiad, id_stage):
    try:
        contests = Contest.query.all()

        all_contests = []

        for contest in contests:
            all_contests.append(
                {
                    "contest_id": contest.contest_id,
                    "description": contest.description,
                    "rules": contest.rules,
                    "winning_condition": contest.winning_condition,
                    "laureate_condition": contest.laureate_condition,
                    "certificate_template": contest.certificate_template,
                    "visibility": contest.visibility,
                    "start_date": contest.start_date,
                    "end_time": contest.end_time,
                    "composite_type": contest.composite_type,
                    "olympiad_type": contest.olympiad_type,
                    "subject": contest.subject,
                    "target_class": contest.target_class,
                }
            )

        return make_response(
            {
                "contests_list": all_contests
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


# Variant views


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/variant/create', methods=['POST'])
@openapi
def variant_create(id_olympiad, id_stage, id_contest):
    try:
        values = request.openapi.body

        contest = Contest.query.filter_by(Contest.contest_id == id_contest).one()
        contest.variants.all()

        variant_description = values['variant_description']

        # TODO Checking

        variant = Variant(
            contest_id=id_contest,
            variant_number=len(contest),
            variant_description=variant_description,
        )
        db.session.add(contest)

        db.session.commit()
        return make_response(
            {
                "variant_id": variant.variant_id,
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/variant/<id_variant>/remove', methods=['POST'])
@openapi
def variant_remove(id_olympiad, id_stage, id_contest, id_variant):
    try:
        variant = Variant.query.filter_by(Variant.variant_id == id_variant).one()
        db.session.delete(variant)
        db.session.commit()
        return make_response({}, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/variant/<variant_num>', methods=['GET'])
@openapi
def variant_get(id_olympiad, id_stage, id_contest, variant_num):
    try:
        variant = Variant.query.filter_by(Variant.contest_id == id_contest).filter_by(Variant.variant_num == variant_num).one()
        return make_response(
            {
                "variant_id": variant.variant_id,
                "variant_number": variant.variant_number,
                "variant_description": variant.variant_description,
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/variant/<variant_num>', methods=['PATCH'])
@openapi
def variant_update(id_olympiad, id_stage, id_contest, variant_num):
    try:
        variant = Variant.query.filter_by(Variant.variant_num == variant_num).one()

        values = request.openapi.body

        if 'variant_number' in values:
            variant.variant_number = values['variant_number']
        if 'variant_description' in values:
            variant.variant_description = values['variant_description']

        db.session.commit()
        return make_response({}, 200)


    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/variant/all', methods=['GET'])
@openapi
def variant_all(id_olympiad, id_stage, id_contest):
    try:
        variants = Variant.query.all()

        all_variants = []

        for variant in variants:
            all_variants.append(
                {
                    "variant_id": variant.variant_id,
                    "variant_number": variant.variant_number,
                    "variant_description": variant.variant_description,
                }
            )

        return make_response(
            {
                "variants_list": all_variants
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()



# Task views


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/variant/<id_variant>/task/create', methods=['POST'])
@openapi
def task_create(id_olympiad, id_stage, id_contest, id_variant):
    try:
        task = None
        values = request.openapi.body

        # TODO Checking
        # TODO Перенести в отдельные функции

        if 'recommended_answer' in values:
            num_of_task = values['num_of_task']
            image_of_task = values['image_of_task']
            recommended_answer = values['image_of_task']
            task = Task(
                num_of_task=num_of_task,
                image_of_task=image_of_task,
                type=TaskType.plain_task,
            )

            db.session.add(task)
            db.session.flush()

            plainTask = PlainTask(
                task_id = task.task_id,
                recommended_answer=recommended_answer,
            )

            db.session.add(plainTask)


        elif 'start_value' in values:
            num_of_task = values['num_of_task']
            image_of_task = values['image_of_task']
            start_value = values['start_value']
            end_value = values['end_value']

            task = Task(
                num_of_task=num_of_task,
                image_of_task=image_of_task,
                type=TaskType.range_task,
            )

            db.session.add(task)
            db.session.flush()

            rangeTask = PlainTask(
                task_id = task.task_id,
                start_value=start_value,
                end_value=end_value,
            )

            db.session.add(rangeTask)

        else:
            num_of_task = values['num_of_task']
            image_of_task = values['image_of_task']
            answers = values['answers']
            task = Task(
                num_of_task=num_of_task,
                image_of_task=image_of_task,
                type=TaskType.multiple_task,
            )

            db.session.add(task)
            db.session.flush()

            multipleTask = MultipleTask(
                task_id = task.task_id,
            )

            db.session.add(multipleTask)

            for answer in answers:
                answerForTask = AnswersInMultipleChoiceTask(
                    task_id = task.task_id,
                    answer = answer['answer'],
                    correct = answer['is_right_answer'],
                )

                db.session.add(answerForTask)


        db.session.commit()
        return make_response(
            {
                "task_id": task.task_id,
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/variant/<id_variant>/task/<id_task>/remove', methods=['POST'])
@openapi
def task_remove(id_olympiad, id_stage, id_contest, id_variant, id_task):
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

            # multipleAnswers = AnswersInMultipleChoiceTask.query.filter_by(AnswersInMultipleChoiceTask.task_id == id_task).all()

            for answer in multipleTask.all_answers_in_multiple_task.all():
                db.session.delete(answer)

            db.session.delete(multipleTask)

        db.session.delete(task)

        db.session.commit()
        return make_response({}, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/variant/<id_variant>/task/<id_task>', methods=['GET'])
@openapi
def task_get(id_olympiad, id_stage, id_contest, id_variant, id_task):
    try:
        task = Task.query.filter_by(Task.task_id == id_task).one()

        if task.type == TaskType.plain_task:
            plainTask = PlainTask.query.filter_by(PlainTask.task_id == id_task).one()

            return make_response(
                {
                    "task_id": task.task_id,
                    "num_of_task": task.num_of_task,
                    "image_of_task": task.image_of_task,
                    "recommended_answer": plainTask.recommended_answer,
                }, 200)

        elif task.type == TaskType.range_task:
            rangeTask = RangeTask.query.filter_by(RangeTask.task_id == id_task).one()

            return make_response(
                {
                    "task_id": task.task_id,
                    "num_of_task": task.num_of_task,
                    "image_of_task": task.image_of_task,
                    "start_value": rangeTask.start_value,
                    "end_value": rangeTask.end_value,
                }, 200)

        elif task.type == TaskType.multiple_task:
            multipleTask = MultipleTask.query.filter_by(MultipleTask.task_id == id_task).one()

            answers = []

            for answer in multipleTask.all_answers_in_multiple_task.all():
                answers.append({
                    'answer': answer.answer,
                    'is_right_answer': answer.correct
                })

            return make_response(
                {
                    "task_id": task.task_id,
                    "num_of_task": task.num_of_task,
                    "image_of_task": task.image_of_task,
                    "answers": answers
                }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/variant/<id_variant>/task/<id_task>', methods=['PATCH'])
@openapi
def task_update(id_olympiad, id_stage, id_contest, id_variant, id_task):
    try:
        task = Task.query.filter_by(Task.task_id == id_task).one()

        values = request.openapi.body

        if 'num_of_task' in values:
            task.num_of_task = values['num_of_task']
        if 'image_of_task' in values:
            task.image_of_task = values['image_of_task']

        if task.type == TaskType.plain_task:
            plainTask = PlainTask.query.filter_by(PlainTask.task_id == id_task).one()

            if 'recommended_answer' in values:
                plainTask.recommended_answer = values['recommended_answer']

        elif task.type == TaskType.plain_task:
            rangeTask = RangeTask.query.filter_by(RangeTask.task_id == id_task).one()

            if 'start_value' in values:
                rangeTask.recommended_answer = values['start_value']
            if 'end_value' in values:
                rangeTask.recommended_answer = values['end_value']

        elif task.type == TaskType.plain_task:
            # multipleTask = MultipleTask.query.filter_by(MultipleTask.task_id == id_task).one()

            if 'answers' in values:
                for answer in answers:
                    answerForTask = AnswersInMultipleChoiceTask.query.filter_by(AnswersInMultipleChoiceTask.answer_id == answer['answer_id']).one()
                    answerForTask.answer = answer['answer']
                    answerForTask.correct = answer['is_right_answer']

        db.session.commit()
        return make_response({}, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/variant/<id_variant>/task/all', methods=['GET'])
@openapi
def task_all(id_olympiad, id_stage, id_contest, id_variant):
    try:
        tasks = Task.query.all()

        all_tasks = []

        for task in tasks:
            all_variants.append(
                {
                    "task_id": task.task_id,
                    "num_of_task": task.num_of_task,
                }
            )

        return make_response(
            {
                "tasks_list": all_tasks
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()



@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/variant/<id_variant>/task/<id_task>/taskimage', methods=['GET'])
@openapi
def task_image(id_olympiad, id_stage, id_contest, id_variant, id_task):
    try:
        tasks = Task.query.filter_by(Task.task_id == id_task).one()

        return make_response(
            {
                "task_id": task.task_id,
                "image_of_task": task.image_of_task
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


# User views

@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/adduser', methods=['POST'])
@openapi
def add_user_to_contest(id_olympiad, id_stage, id_contest):
    try:
        values = request.openapi.body

        users_id = values['users_id']

        # TODO Checking

        for user_id in users_id:
            user = UserInContest(
                user_id=user_id,
                contest_id=id_contest,
                variant_id= None, #TODO
                user_status = None #TODO

            )

            db.session.add(user)

        db.session.commit()
        return make_response(
            {
                "users_id": users_id,
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/{id_contest}/removeuser:', methods=['POST'])
@openapi
def remove_user_from_contest(id_olympiad, id_stage, id_contest):
    try:
        values = request.openapi.body

        users_id = values['users_id']

        # TODO Checking

        for user_id in users_id:
            user = UserInContest.query.filter_by(UserInContest.user_id == user_id).one()
            db.session.delete(user)

        db.session.commit()
        return make_response({}, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/{id_contest}/user/all', methods=['GET'])
@openapi
def users_all(id_olympiad, id_stage, id_contest):
    try:
        users = UserInContest.query.filter_by(UserInContest.contest_id == id_contest).one()

        all_users = []

        for user in users:
            all_users.append(
                {
                    "user_id": user.user_id,
                    "variant_id": user.variant_id,
                    "user_status": user.user_status,
                }
            )

        return make_response(
            {
                "user_list": all_users
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/{id_contest}/user/<id_user>/certificate', methods=['GET'])
@openapi
def users_all(id_olympiad, id_stage, id_contest, id_user):
    try:
        user = UserInContest.query.filter_by(UserInContest.user_id == id_user).one()

        contest = Contest.query.filter_by(Contest.contest_id == id_contest).one()

        # TODO Function
        certificate = getCertificateFromTemplate(user, contest.certificate_template)

        return make_response(
            {
                "certificate": certificate
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()