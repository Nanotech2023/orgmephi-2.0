import datetime

from flask import request, make_response
import re

from contest_data.models_task import *
from contest_data.errors import *
from contest_data import app, db, openapi


# Olympiad views

@app.route('/olympiad/create', methods=['POST'])
@openapi
def olympiad_create():
    try:
        values = request.openapi.body
        name = values['name']
        desc = values['description']
        rules = values['rules']

        # TODO Checking

        olympiad = Olympiad(
            name=name,
            description=desc,
            rules=rules,
        )
        db.session.add(olympiad)

        # Generate olympiad.id
        # db.session.flush()

        db.session.commit()
        return make_response(
            {
                "olympiad_id": olympiad.olympiad_id,
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()

@app.route('/olympiad/<id_olympiad>/remove', methods=['POST'])
@openapi
def olympiad_remove(id_olympiad):
    try:
        olympiad = Olympiad.query.filter_by(Olympiad.olympiad_id == id_olympiad).one()
        db.session.delete(olympiad)
        db.session.commit()
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
        )
        db.session.add(contest)

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

        db.session.commit()

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
    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/variant/<id_variant>', methods=['GET'])
@openapi
def variant_get(id_olympiad, id_stage, id_contest, id_variant):
    try:
        variant = Variant.query.filter_by(Variant.variant_id == id_variant).one()
        return make_response(
            {
                "variant_id": variant.variant_id,
                "variant_number": variant.variant_number,
                "variant_description": variant.variant_description,
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()


@app.route('/olympiad/<id_olympiad>/stage/<id_stage>/contest/<id_contest>/variant/<id_variant>', methods=['PATCH'])
@openapi
def variant_update(id_olympiad, id_stage, id_contest, id_variant):
    try:
        variant = Variant.query.filter_by(Variant.variant_id == id_variant).one()

        values = request.openapi.body

        if 'variant_number' in values:
            variant.variant_number = values['variant_number']
        if 'variant_description' in values:
            variant.variant_description = values['variant_description']

        db.session.commit()

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