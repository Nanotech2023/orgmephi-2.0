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
def olympiad_update():
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
                "olympiad_list:": all_olympiads
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
def olympiad_update():
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
                "stages_list::": all_stages
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()