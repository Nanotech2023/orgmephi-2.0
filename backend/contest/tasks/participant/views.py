from flask import abort, make_response

from common import get_current_app, get_current_module
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


# Variant

@module.route(
    '/contest/<int:id_contest>/variant/self',
    methods=['GET'])
def variant_self(id_contest):
    """
    Get variant for user in current contest
    """
    variant = get_user_variant_if_possible(id_contest)
    return make_response(
        variant.serialize(), 200)


# Task


@module.route(
    '/contest/<int:id_contest>/tasks/self',
    methods=['GET'])
def task_all(id_contest):
    """
    Get tasks for user in current variant
    """
    tasks = get_user_tasks_if_possible(id_contest)
    return make_response(
        {
            "tasks_list": tasks
        }, 200)


@module.route(
    '/contest/<int:id_contest>/tasks/<int:id_task>/self',
    methods=['GET'])
def task_get(id_contest, id_task):
    """
    Get task for user in current variant
    """
    task = get_user_task_if_possible(id_contest, id_task)
    return make_response(
        task.serialize(), 200)


@module.route(
    '/contest/<int:id_contest>/tasks/<int:id_task>/image/self',
    methods=['GET'])
def task_image(id_contest, id_task):
    """
    Get task image for user in current task
    """
    task = get_user_task_if_possible(id_contest, id_task)
    return make_response(
        task.serialize_image(), 200)


# Certificate


@module.route(
    '/contest/<int:id_contest>/certificate/self',
    methods=['GET'])
def users_certificate(id_contest):
    # contest = get_user_contest_if_possible(id_contest)
    # certificate = None
    abort(502)
