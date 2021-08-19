from common.errors import InsufficientData
from common.util import db_get_or_raise
from common.jwt_verify import jwt_get_id

from contest.tasks.models import *

import random

# Generators


def get_last_variant_in_contest(contest):
    variants = contest.variants.all()
    if len(variants) > 0:
        new_variant = max(variant.variant_number for variant in variants)
    else:
        new_variant = 0

    return new_variant


def generate_variant(id_contest, user_id):
    contest = db_get_or_raise(Contest, "contest_id", id_contest)
    variants_number = len(contest.variants.all())
    if variants_number == 0:
        raise InsufficientData('variant', 'variants in contest')
    random_number = random.randint(0, variants_number * 2)
    variant = (user_id + random_number) % variants_number
    return variant

# Functions for tasks/participant


def is_user_in_contest(user_id, contest):
    if contest.users.filter_by(**{"user_id": str(user_id)}).one_or_none() is not None:
        return True
    else:
        return False


def is_variant_in_contest(variant_id, contest):
    if contest.variants.filter_by(**{"variant_id": str(variant_id)}).one_or_none() is not None:
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
    olympiad = db_get_or_raise(Contest, "contest_id", id_olympiad)
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    if stage not in olympiad.stages:
        raise InsufficientData('stage_id', 'not in current olympiad')
    contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    if contest not in stage.contests:
        raise InsufficientData('contest_id', 'not in current stage')
    if not is_user_in_contest(jwt_get_id(), contest):
        raise InsufficientData('contest_id', 'not in your contests list')
    return contest


def get_user_variant_if_possible(id_contest):
    contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    if contest.composite_type == ContestTypeEnum.CompositeContest:
        raise InsufficientData('composite_type', 'not Simple contest')
    user = db_get_or_raise(UserInContest, "user_id", jwt_get_id())
    variant = contest.variants.filter_by(**{"variant_id": str(user.variant_id)}).one_or_none()
    if variant is None:
        raise InsufficientData("variant_id", "not in this contest")
    if not is_variant_in_contest(variant.variant_id, contest):
        raise InsufficientData('variant_id', 'not in current contests')
    return variant


def get_user_tasks_if_possible(id_contest):
    variant = get_user_variant_if_possible(id_contest)

    for task in variant.tasks:
        if 'answers' in task:
            task.answers = [answer['is_right_answer'] for answer in task.answers]

    tasks = [task for task in variant.tasks]
    return tasks


def get_user_task_if_possible(id_contest, id_task):
    variant = get_user_variant_if_possible(id_contest)
    if is_task_in_variant(id_task, variant):
        task = db_get_or_raise(Task, "task_id", str(id_task))
        return task
    else:
        raise InsufficientData('task_id', 'not in current variant')


# Functions for tasks/contest

def get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest):
    olympiad = db_get_or_raise(Contest, "contest_id", id_olympiad)
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    if stage not in olympiad.stages:
        raise InsufficientData('stage_id', 'not in current olympiad')
    if contest not in stage.contests:
        raise InsufficientData('contest_id', 'not in current stage')
    return contest


def get_contest_if_possible(id_contest):
    contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    return contest


def get_variant_if_possible(id_contest, id_variant):
    contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    variant = contest.variants.filter_by(**{"variant_id": str(id_variant)}).one_or_none()
    if not is_variant_in_contest(variant.variant_id, contest):
        raise InsufficientData('variant_id', 'not in current contests')
    return variant


def get_variant_if_possible_by_number(id_contest, variant_num):
    contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    variant = contest.variants.filter_by(**{"variant_number": str(variant_num)}).one_or_none()
    if variant is None:
        raise InsufficientData("variant_number", "not in this contest")
    if not is_variant_in_contest(variant.variant_id, contest):
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
