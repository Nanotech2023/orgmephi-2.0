import random

from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from common.errors import InsufficientData, TooBigFileSize
from common.jwt_verify import jwt_get_id
from contest.tasks.models import *

# Constants


MAX_FILE_SIZE = 1e7


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


def get_base_contest(current_contest):
    if current_contest.base_contest is not None:
        return current_contest.base_contest

    stage = current_contest.stage[0]
    current_olympiad = db_get_or_raise(Contest, "contest_id", str(stage.olympiad_id))

    return current_olympiad.base_contest


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


# Schema


class FilterOlympiadAllRequestSchema(Schema):
    base_contest_id = fields.Integer()
    location_id = fields.Integer()
    target_classes = EnumField(enum=TargetClassEnum, by_value=True)
    end_date = fields.DateTime()
    only_count = fields.Boolean()
    offset = fields.Integer()
    limit = fields.Integer()


_filter_fields = ['base_contest_id', 'location_id', 'target_classes', 'end_date']


# Olympiad filter

def filter_olympiad_query(args):
    marshmallow = FilterOlympiadAllRequestSchema().load(args)

    filters = {v: marshmallow[v] for v in _filter_fields if v in marshmallow}

    query = SimpleContest.query.filter_by(**filters)

    offset = marshmallow.get('offset', None)
    limit = marshmallow.get('limit', None)
    if offset is not None:
        query = query.order_by(SimpleContest.start_date)
    if limit is not None:
        query = query.offset(offset).limit(limit)
    if marshmallow.get('only_count', False):
        return {'count': query.count()}, 200
    else:
        return {'contest_list': query.all(), 'count': query.count()}, 200


def validate_file_size(binary_file):
    if len(binary_file) > MAX_FILE_SIZE:
        raise TooBigFileSize()
