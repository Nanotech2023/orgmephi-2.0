import secrets

from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from common import get_current_app
from common.errors import InsufficientData, FileTooLarge, DataConflict
from common.jwt_verify import jwt_get_id
from contest.tasks.models import *

app = get_current_app()


# Constants


# Generators


def get_last_variant_in_contest(current_contest):
    """
    Get last variant number in current contest
    :param current_contest:
    :return:
    """
    variants = current_contest.variants.all()
    if len(variants) > 0:
        return max(variant.variant_number for variant in variants)
    else:
        return 0


def generate_variant(contest_id, user_id):
    """
    Generate random variant number for user
    :param contest_id:
    :param user_id:
    :return:
    """
    current_contest = db_get_or_raise(Contest, "contest_id", contest_id)
    variant_numbers_list = [variant.variant_number for variant in current_contest.variants.all()]
    variants_amount = len(variant_numbers_list)
    if variants_amount == 0:
        raise DataConflict('No variants found in current contest')
    random_number = secrets.randbelow(variants_amount * 420)
    final_variant_number = variant_numbers_list[(user_id + random_number) % variants_amount]
    return final_variant_number


# Functions for tasks/participant


def is_user_in_contest(user_id, current_contest):
    """
    Check if user in current contest
    :param user_id:
    :param current_contest:
    :return:
    """
    return current_contest.users.filter_by(**{"user_id": str(user_id)}).one_or_none() is not None


def is_variant_in_contest(variant_id, current_contest):
    """
    Check if variant in contest
    :param variant_id:
    :param current_contest:
    :return:
    """
    return current_contest.variants.filter_by(**{"variant_id": str(variant_id)}).one_or_none() is not None


def is_task_in_variant(task_id, variant):
    """
    Check if task in current variant
    :param task_id:
    :param variant:
    :return:
    """
    task = db_get_or_raise(Task, "task_id", task_id)
    return task in variant.tasks


def is_task_in_contest(task_id, contest_id):
    """
    Check if task in contest
    :param task_id:
    :param contest_id:
    :return:
    """

    current_contest = db_get_or_raise(Contest, "contest_id", contest_id)
    task = db_get_or_raise(Task, "task_id", task_id)
    task_variant = task.variant
    if task_variant is None:
        raise DataConflict("Task variant is missing")
    return task_variant in current_contest.variants


def get_user_contest_if_possible(olympiad_id, stage_id, contest_id):
    current_olympiad = db_get_or_raise(Contest, "contest_id", olympiad_id)
    if current_olympiad.composite_type == ContestTypeEnum.SimpleContest:
        raise InsufficientData('composite_type', 'not Composite contest')
    stage = db_get_or_raise(Stage, "stage_id", str(stage_id))
    if stage not in current_olympiad.stages:
        raise InsufficientData('stage_id', 'not in current olympiad')
    current_contest = db_get_or_raise(Contest, "contest_id", str(contest_id))
    if current_contest not in stage.contests:
        raise InsufficientData('contest_id', 'not in current stage')
    if not is_user_in_contest(jwt_get_id(), current_contest):
        raise DataConflict("User is not registered for this olympiad")
    return current_contest


def get_user_variant_if_possible(contest_id):
    current_contest = db_get_or_raise(Contest, "contest_id", str(contest_id))
    if current_contest.composite_type == ContestTypeEnum.CompositeContest:
        raise InsufficientData('composite_type', 'not Simple contest')
    current_user = db_get_or_raise(UserInContest, "user_id", jwt_get_id())
    variant = current_contest.variants.filter_by(**{"variant_id": str(current_user.variant_id)}).one_or_none()
    if variant is None:
        raise InsufficientData("variant_id", "not in this contest")
    if not is_variant_in_contest(variant.variant_id, current_contest):
        raise InsufficientData('variant_id', 'not in current contests')
    return variant


def get_user_tasks_if_possible(contest_id):
    variant = get_user_variant_if_possible(contest_id)

    current_tasks = variant.tasks[:]

    for task in current_tasks:
        if task.task_type == TaskTypeEnum.MultipleChoiceTask:
            task.answers = [answer['is_right_answer'] for answer in task.answers]

    return current_tasks


def get_user_task_if_possible(contest_id, task_id):
    variant = get_user_variant_if_possible(contest_id)
    if is_task_in_variant(task_id, variant):
        task = db_get_or_raise(Task, "task_id", str(task_id))
        return task
    else:
        raise InsufficientData('task_id', 'not in current variant')


# Functions for tasks/contest

def get_contest_if_possible_from_stage(olympiad_id, stage_id, contest_id):
    current_olympiad = db_get_or_raise(Contest, "contest_id", olympiad_id)
    if current_olympiad.composite_type == ContestTypeEnum.SimpleContest:
        raise InsufficientData('composite_type', 'not Composite contest')
    stage = db_get_or_raise(Stage, "stage_id", str(stage_id))
    current_contest = db_get_or_raise(Contest, "contest_id", str(contest_id))
    if stage not in current_olympiad.stages:
        raise InsufficientData('stage_id', 'not in current olympiad')
    if current_contest not in stage.contests:
        raise InsufficientData('contest_id', 'not in current stage')
    return current_contest


def get_contest_if_possible(contest_id):
    current_contest = db_get_or_raise(Contest, "contest_id", str(contest_id))
    return current_contest


def get_base_contest(current_contest):
    if current_contest.base_contest is not None:
        return current_contest.base_contest

    stage = current_contest.stage[0]
    current_olympiad = db_get_or_raise(Contest, "contest_id", str(stage.olympiad_id))

    return current_olympiad.base_contest


def get_variant_if_possible(contest_id, variant_id):
    """
    Get variant by id
    :param contest_id: Simple contest
    :param variant_id:id variant
    :return:
    """
    current_contest = db_get_or_raise(Contest, "contest_id", str(contest_id))
    if current_contest.composite_type == ContestTypeEnum.CompositeContest:
        raise InsufficientData('composite_type', 'not Simple contest')
    variant = current_contest.variants.filter_by(**{"variant_id": str(variant_id)}).one_or_none()
    if not is_variant_in_contest(variant.variant_id, current_contest):
        raise InsufficientData('variant_id', 'not in current contests')
    return variant


def get_variant_if_possible_by_number(contest_id, variant_num):
    """
    Get variant by num
    :param contest_id: Simple contest
    :param variant_num: variant num
    :return:
    """
    current_contest = db_get_or_raise(Contest, "contest_id", str(contest_id))
    if current_contest.composite_type == ContestTypeEnum.CompositeContest:
        raise InsufficientData('composite_type', 'not Simple contest')
    variant = current_contest.variants.filter_by(**{"variant_number": str(variant_num)}).one_or_none()
    if variant is None:
        raise InsufficientData("variant_number", "not in this contest")
    if not is_variant_in_contest(variant.variant_id, current_contest):
        raise InsufficientData('variant_number', 'not in current contests')
    return variant


def get_tasks_if_possible(contest_id, variant_id):
    variant = get_variant_if_possible(contest_id, variant_id)
    return variant.tasks


def get_task_if_possible(contest_id, variant_id, task_id):
    variant = get_variant_if_possible(contest_id, variant_id)
    if is_task_in_variant(task_id, variant):
        task = db_get_or_raise(Task, "task_id", str(task_id))
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


_filter_fields = ['base_contest_id', 'location_id', 'end_date']


# Olympiad filter

def filter_olympiad_query(args):
    marshmallow = FilterOlympiadAllRequestSchema().load(args)

    filters = {v: marshmallow[v] for v in _filter_fields if v in marshmallow}

    query = SimpleContest.query.filter_by(**filters)

    offset = marshmallow.get('offset', None)
    limit = marshmallow.get('limit', None)

    # TODO Target classes filtering
    # target_classes = marshmallow.get('target_classes', None)
    # if target_classes is not None:
    #    ..

    query = query.order_by(SimpleContest.start_date)

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    if marshmallow.get('only_count', False):
        return {'count': query.count()}, 200
    else:
        return {'contest_list': query.all(), 'count': query.count()}, 200


def validate_file_size(binary_file):
    if len(binary_file) > app.config['ORGMEPHI_MAX_FILE_SIZE']:
        raise FileTooLarge()
