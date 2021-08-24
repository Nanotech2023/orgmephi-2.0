from common.errors import InsufficientData
from common.util import db_get_or_raise
from common.jwt_verify import jwt_get_id

from contest.tasks.models import *

import random

# Generators


def get_last_variant_in_contest(current_contest):
    variants = current_contest.variants.all()
    if len(variants) > 0:
        new_variant = max(variant.variant_number for variant in variants)
    else:
        new_variant = 0

    return new_variant


def generate_variant(id_contest, user_id):
    current_contest = db_get_or_raise(Contest, "contest_id", id_contest)
    variants_number = len(current_contest.variants.all())
    if variants_number == 0:
        raise InsufficientData('variant', 'variants in contest')
    random_number = random.randint(0, variants_number * 2)
    variant = (user_id + random_number) % variants_number
    return variant

# Functions for tasks/participant


def is_user_in_contest(user_id, current_contest):
    if current_contest.users.filter_by(**{"user_id": str(user_id)}).one_or_none() is not None:
        return True
    else:
        return False


def is_variant_in_contest(variant_id, current_contest):
    if current_contest.variants.filter_by(**{"variant_id": str(variant_id)}).one_or_none() is not None:
        return True
    else:
        return False


def is_task_in_variant(task_id, variant):
    task = db_get_or_raise(Task, "task_id", task_id)
    if task in variant.tasks:
        return True
    else:
        return False


def get_user_contest_if_possible(id_olympiad, id_stage, id_contest):
    current_olympiad = db_get_or_raise(Contest, "contest_id", id_olympiad)
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    if stage not in current_olympiad.stages:
        raise InsufficientData('stage_id', 'not in current olympiad')
    current_contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    if current_contest not in stage.contests:
        raise InsufficientData('contest_id', 'not in current stage')
    if not is_user_in_contest(jwt_get_id(), current_contest):
        raise InsufficientData('contest_id', 'not in your contests list')
    return current_contest


def get_user_variant_if_possible(id_contest):
    current_contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    if current_contest.composite_type == ContestTypeEnum.CompositeContest:
        raise InsufficientData('composite_type', 'not Simple contest')
    current_user = db_get_or_raise(UserInContest, "user_id", jwt_get_id())
    variant = current_contest.variants.filter_by(**{"variant_id": str(current_user.variant_id)}).one_or_none()
    if variant is None:
        raise InsufficientData("variant_id", "not in this contest")
    if not is_variant_in_contest(variant.variant_id, current_contest):
        raise InsufficientData('variant_id', 'not in current contests')
    return variant


def get_user_tasks_if_possible(id_contest):
    variant = get_user_variant_if_possible(id_contest)

    current_tasks = variant.tasks[:]

    for task in current_tasks:
        if task.task_type == TaskTypeEnum.MultipleChoiceTask:
            task.answers = [answer['is_right_answer'] for answer in task.answers]

    return current_tasks


def get_user_task_if_possible(id_contest, id_task):
    variant = get_user_variant_if_possible(id_contest)
    if is_task_in_variant(id_task, variant):
        task = db_get_or_raise(Task, "task_id", str(id_task))
        return task
    else:
        raise InsufficientData('task_id', 'not in current variant')


# Functions for tasks/contest

def get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest):
    current_olympiad = db_get_or_raise(Contest, "contest_id", id_olympiad)
    if current_olympiad.composite_type == ContestTypeEnum.SimpleContest:
        raise InsufficientData('composite_type', 'not Composite contest')
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    current_contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    if stage not in current_olympiad.stages:
        raise InsufficientData('stage_id', 'not in current olympiad')
    if current_contest not in stage.contests:
        raise InsufficientData('contest_id', 'not in current stage')
    return current_contest


def get_contest_if_possible(id_contest):
    current_contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    return current_contest


def get_variant_if_possible(id_contest, id_variant):
    """
    Get variant by id
    :param id_contest: Simple contest
    :param id_variant:id variant
    :return:
    """
    current_contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    if current_contest.composite_type == ContestTypeEnum.CompositeContest:
        raise InsufficientData('composite_type', 'not Simple contest')
    variant = current_contest.variants.filter_by(**{"variant_id": str(id_variant)}).one_or_none()
    if not is_variant_in_contest(variant.variant_id, current_contest):
        raise InsufficientData('variant_id', 'not in current contests')
    return variant


def get_variant_if_possible_by_number(id_contest, variant_num):
    """
    Get variant by num
    :param id_contest: Simple contest
    :param variant_num: variant num
    :return:
    """
    current_contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    if current_contest.composite_type == ContestTypeEnum.CompositeContest:
        raise InsufficientData('composite_type', 'not Simple contest')
    variant = current_contest.variants.filter_by(**{"variant_number": str(variant_num)}).one_or_none()
    if variant is None:
        raise InsufficientData("variant_number", "not in this contest")
    if not is_variant_in_contest(variant.variant_id, current_contest):
        raise InsufficientData('variant_number', 'not in current contests')
    return variant


def get_tasks_if_possible(id_contest, id_variant):
    variant = get_variant_if_possible(id_contest, id_variant)
    return variant.tasks


def get_task_if_possible(id_contest, id_variant, id_task):
    variant = get_variant_if_possible(id_contest, id_variant)
    if is_task_in_variant(id_task, variant):
        task = db_get_or_raise(Task, "task_id", str(id_task))
        return task
    else:
        raise InsufficientData('task_id', 'not in current variant')


# Validators

def validate_contest_values(previous_contest_id, previous_participation_condition):
    if (previous_participation_condition is None and previous_contest_id is not None) or \
            (previous_participation_condition is not None and previous_contest_id is None):
        raise InsufficientData("previous_contest_id", "id or condition")
