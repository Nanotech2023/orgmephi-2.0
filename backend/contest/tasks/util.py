import io
import secrets

from common.errors import FileTooLarge, DataConflict, InsufficientData, RequestError, NotFound
from common.jwt_verify import jwt_get_id
from contest.tasks.models import *
from contest.tasks.unauthorized.schemas import FilterOlympiadAllRequestSchema
from user.models import UserTypeEnum

app = get_current_app()


# Contest getters


def get_previous_contest_if_possible(current_contest):
    """
    Get contest
    :param current_contest: current contest
    :return: contest
    """
    if current_contest.previous_contest_id is not None:
        return db_get_or_raise(Contest, "contest_id", str(current_contest.previous_contest_id))
    else:
        return None


def compare_conditions_weights(current_contest, prev_contest, user_id):
    """
    Compare conditions weights
    :param current_contest: current contest
    :param prev_contest: prev contest
    :param user_id: user id
    :return:
    """
    participation_condition_weight = user_status_weights_dict[
        current_contest.previous_participation_condition.value]
    user_in_contest_status_weight = user_status_weights_dict[
        get_user_in_contest_by_id_if_possible(prev_contest.contest_id, user_id).user_status.value]

    return user_in_contest_status_weight >= participation_condition_weight


def _get_passed(simple_contest, user_id):
    """
    Get passed
    :param simple_contest:
    :return:
    """
    if simple_contest.previous_participation_condition is None:
        return True
    prev_contest: SimpleContest = get_previous_contest_if_possible(simple_contest)
    return compare_conditions_weights(simple_contest, prev_contest, user_id)


def check_stage_condition(prev_contest, user_id, current_step_condition):
    """
    Check enrollment to the next stage condition
    :param prev_contest: prev contest
    :param user_id: user if
    :param current_step_condition: current step condition
    :return:
    """
    prev_stage = prev_contest.stage
    if prev_stage is None:
        return current_step_condition
    condition = prev_stage.condition

    passed_list = (_get_passed(simple_contest, user_id) for simple_contest in prev_stage.contests)
    if condition == StageConditionEnum.And:
        return all(passed_list)
    elif condition == StageConditionEnum.Or:
        return any(passed_list)

    return current_step_condition


def check_previous_contest_condition_if_possible(contest_id, user_id):
    """
    Check contest condition
    :param user_id: user id
    :param contest_id: contest id
    :return: contest
    """
    current_contest = db_get_or_raise(Contest, "contest_id", str(contest_id))
    prev_contest = get_previous_contest_if_possible(current_contest)
    if prev_contest is None:
        return True

    current_step_condition = compare_conditions_weights(current_contest, prev_contest, user_id)
    current_stage_step_condition = check_stage_condition(prev_contest, user_id, current_step_condition)

    if current_contest.stage is not None and prev_contest.stage is not None:
        if current_contest.stage.stage_num == prev_contest.stage.stage_num:
            return current_step_condition
        else:
            return current_stage_step_condition
    elif prev_contest.stage is not None:
        return current_stage_step_condition
    else:
        return current_step_condition


def get_contest_if_possible(contest_id):
    """
    Get contest
    :param contest_id: contest id
    :return: contest
    """
    current_contest = db_get_or_raise(Contest, "contest_id", str(contest_id))
    return current_contest


def get_simple_contest_if_possible(contest_id):
    """
    Get simple contest
    :param contest_id: contest id
    :return: simple contest
    """
    current_contest = db_get_or_raise(Contest, "contest_id", str(contest_id))
    if current_contest.composite_type == ContestTypeEnum.CompositeContest:
        raise DataConflict('Current contest type is not simple one')
    return current_contest


def get_composite_contest_if_possible(contest_id):
    """
    Get composite contest
    :param contest_id: contest id
    :return: composite contest
    """
    current_contest = db_get_or_raise(Contest, "contest_id", str(contest_id))
    if current_contest.composite_type == ContestTypeEnum.SimpleContest:
        raise DataConflict('Current contest type is not composite one')
    return current_contest


# Constants


# Generators


def get_last_variant_in_contest(current_contest):
    """
    Get last variant number in current contest
    :param current_contest: current contest
    :return: max number of the variant
    """
    variants = current_contest.variants.all()
    if len(variants) > 0:
        return max(variant.variant_number for variant in variants)
    else:
        return 0


def generate_variant(contest_id, user_id):
    """
    Generate random variant number for user
    :param contest_id: contest id
    :param user_id: user id
    :return: final variant number
    """
    current_contest = db_get_or_raise(Contest, "contest_id", contest_id)
    variant_id_list = [variant.variant_id for variant in current_contest.variants.all()]
    variants_amount = len(variant_id_list)
    if variants_amount == 0:
        raise DataConflict('No variants found in current contest')
    random_number = secrets.randbelow(variants_amount * 420)
    final_variant_number = variant_id_list[(user_id + random_number) % variants_amount]
    return final_variant_number


# User module


def is_stage_in_contest(current_olympiad, stage):
    if current_olympiad.composite_type != ContestTypeEnum.CompositeContest or stage not in current_olympiad.stages:
        raise InsufficientData('stage_id', 'not in current olympiad')
    else:
        return True


def is_user_in_contest(user_id, current_contest):
    """
    Check if user in current contest
    :param user_id: user id
    :param current_contest: current contest
    :return: boolean value if user in current contest
    """
    return current_contest.users.filter_by(user_id=str(user_id)).one_or_none() is not None


# Contest content module

def is_task_in_variant(task_id, variant):
    """
    Check if task in current variant
    :param task_id: task id
    :param variant: current variant
    :return: boolean value if task in current variant
    """
    task = db_get_or_raise(Task, "task_id", task_id)
    return task in variant.tasks


def is_task_in_contest(task_id, contest_id):
    """
    Check if task in contest
    :param task_id: task id
    :param contest_id: contest id
    :return: boolean value if task in contest
    """

    current_contest = db_get_or_raise(Contest, "contest_id", contest_id)
    task = db_get_or_raise(Task, "task_id", task_id)
    task_variant = task.variant
    if task_variant is None:
        raise DataConflict("Task variant is missing")
    contest_variants = current_contest.variants.all()
    for var in task_variant:
        if var in contest_variants:
            return True
    return False


# Participant module


def get_contest_for_participant_if_possible(olympiad_id, stage_id, contest_id):
    """
    Get contest for user or raise exception
    :param olympiad_id:
    :param stage_id:
    :param contest_id:
    :return: user contest
    """
    current_olympiad = get_composite_contest_if_possible(olympiad_id)

    stage = db_get_or_raise(Stage, "stage_id", str(stage_id))

    # stage is not in current olympiad
    if stage not in current_olympiad.stages:
        raise DataConflict("Stage is not in current olympiad")

    current_contest = db_get_or_raise(Contest, "contest_id", str(contest_id))

    # contest is not in stage
    if current_contest not in stage.contests:
        raise DataConflict("Current contest is not in chosen stage")

    return current_contest


def get_user_contest_if_possible(olympiad_id, stage_id, contest_id):
    """
    Get contest for user or raise exception
    :param olympiad_id:
    :param stage_id:
    :param contest_id:
    :return: user contest
    """
    current_contest = db_get_or_raise(Contest, "contest_id", str(contest_id))

    # user is not registered
    if not is_user_in_contest(jwt_get_id(), current_contest):
        raise DataConflict("User is not registered for this olympiad")

    return get_contest_for_participant_if_possible(olympiad_id, stage_id, contest_id)


def get_user_simple_contest_if_possible(olympiad_id):
    """
    Get contest for user or raise exception
    :param olympiad_id:
    :return: user contest
    """
    current_olympiad = get_simple_contest_if_possible(olympiad_id)

    # user is not registered
    if not is_user_in_contest(jwt_get_id(), current_olympiad):
        raise DataConflict("User is not registered for this olympiad")

    return current_olympiad


def get_user_in_contest_by_id_if_possible(contest_id, user_id) -> UserInContest:
    """
    Get contest for user or raise exception
    :param user_id: user id
    :param contest_id: contest id
    :return: user contest
    """
    current_contest = get_simple_contest_if_possible(contest_id)

    # user is not registered
    if not is_user_in_contest(user_id, current_contest):
        raise NotFound("user_id", str(user_id))

    return current_contest.users.filter_by(**{"user_id": user_id,
                                              "contest_id": contest_id}).one_or_none()


def get_user_variant_if_possible(contest_id):
    """
    Get user variant if possible
    :param contest_id:
    :return: user variant
    """
    current_contest = get_simple_contest_if_possible(contest_id)

    current_user = get_user_in_contest_by_id_if_possible(contest_id, jwt_get_id())
    variant = current_contest.variants.filter_by(variant_id=str(current_user.variant_id)).one_or_none()

    # no variant in user profile
    if variant is None:
        raise DataConflict('User isn\'t linked with any variant')

    return variant


def get_user_tasks_if_possible(contest_id):
    """
    Get user tasks if possible (in contest)
    :param contest_id:
    :return: user task
    """

    variant = get_user_variant_if_possible(contest_id)

    tasks_list = variant.tasks[:]

    for task in tasks_list:
        if task.task_type == TaskTypeEnum.MultipleChoiceTask:
            task.answers = [answer['is_right_answer'] for answer in task.answers]

    return tasks_list


def get_user_task_if_possible(contest_id, task_id):
    """
    Get user task if possible
    :param contest_id: contest id
    :param task_id: task id
    :return: user tasks
    """

    variant = get_user_variant_if_possible(contest_id)
    if is_task_in_variant(task_id, variant):
        task = db_get_or_raise(Task, "task_id", str(task_id))
        return task
    else:
        raise DataConflict('Task is not in current variant')


def get_contest_if_possible_from_stage(olympiad_id, stage_id, contest_id):
    """
    Get contest if possible (from stage)
    :param olympiad_id: olympiad id
    :param stage_id: stage id
    :param contest_id: contest id
    :return: contest
    """

    current_olympiad = get_composite_contest_if_possible(olympiad_id)

    stage = db_get_or_raise(Stage, "stage_id", str(stage_id))

    if stage not in current_olympiad.stages:
        raise DataConflict('Stage is not current olympiad')

    current_contest = db_get_or_raise(Contest, "contest_id", str(contest_id))

    if current_contest not in stage.contests:
        raise DataConflict('Contest is not current stage')

    return current_contest


def get_base_contest(current_contest):
    """
    Get base contest
    :param current_contest: current contest
    :return: base contest
    """

    # If current contest doesn't have base contest
    if current_contest.base_contest is not None:
        return current_contest.base_contest

    stage = current_contest.stage
    current_olympiad = db_get_or_raise(Contest, "contest_id", str(stage.olympiad_id))

    return current_olympiad.base_contest


def get_variant_if_possible(contest_id, variant_id):
    """
    Get variant by id
    :param contest_id: Simple contest
    :param variant_id:id variant
    :return:
    """
    current_contest = get_simple_contest_if_possible(contest_id)

    variant = current_contest.variants.filter_by(variant_id=str(variant_id)).one_or_none()

    return variant


def get_variant_if_possible_by_number(contest_id, variant_num):
    """
    Get variant by num
    :param contest_id: Simple contest
    :param variant_num: variant num
    :return:
    """
    current_contest = get_simple_contest_if_possible(contest_id)

    variant = current_contest.variants.filter_by(variant_number=str(variant_num)).one_or_none()

    if variant is None:
        raise DataConflict('No variants in this contest')

    return variant


def get_tasks_if_possible(contest_id, variant_id):
    """
    Get tasks if possible
    :param contest_id: contest id
    :param variant_id: variant id
    :return: tasks
    """
    variant = get_variant_if_possible(contest_id, variant_id)
    return variant.tasks


def get_task_if_possible(contest_id, variant_id, task_id):
    """
    Get task if possible
    :param contest_id: contest id
    :param variant_id: variant id
    :param task_id: task id
    :return: task
    """
    variant = get_variant_if_possible(contest_id, variant_id)
    if is_task_in_variant(task_id, variant):
        task = db_get_or_raise(Task, "task_id", str(task_id))
        return task
    else:
        raise DataConflict('Task not in current variant')


# Validators

def validate_contest_values(previous_contest_id, previous_participation_condition):
    """
    Check previous contest conditions
    :param previous_contest_id:
    :param previous_participation_condition:
    :return:
    """
    if (previous_participation_condition is None and previous_contest_id is not None) or \
            (previous_participation_condition is not None and previous_contest_id is None):
        raise DataConflict('Can\t create contest with only one of following attributes: previous_contest_id, '
                           'previous_participation_condition')


def user_can_view_variants_and_tasks(id_contest):
    """
    Check if user can view variants and tasks
    :param id_contest:
    :return:
    """
    from contest.responses.models import ResponseStatusEnum
    from contest.responses.util import get_user_in_contest_work
    current_user = get_user_in_contest_by_id_if_possible(id_contest, jwt_get_id())
    current_response = get_user_in_contest_work(str(jwt_get_id()), id_contest)

    # Show task after contest
    current_contest: SimpleContest = get_contest_if_possible(id_contest)
    results_published = datetime.utcnow() >= current_contest.result_publication_date
    show_result = results_published and ResponseStatusEnum.accepted == current_response.work_status and \
                  current_user.show_results_to_user

    return current_response.status == ResponseStatusEnum.in_progress or show_result


# Schema


def validate_file_size(binary_file):
    """
    Check size of binary file
    :param binary_file:  file
    :return: size
    """
    if len(binary_file) > app.config['ORGMEPHI_MAX_FILE_SIZE']:
        raise FileTooLarge()


def check_user_unfilled_for_enroll(current_user: User):
    """
    Check user unfilled for enroll
    :param current_user:
    :return: grade
    """
    unfilled = current_user.unfilled()

    if current_user.type == UserTypeEnum.university:
        if len(unfilled) > 0:
            raise InsufficientData('user.student_info', str(unfilled))
        grade = db_get_or_raise(TargetClass, "target_class", 'student')
    elif current_user.type == UserTypeEnum.school:
        if len(unfilled) > 0:
            raise InsufficientData('user.school_info', str(unfilled))
        grade = db_get_or_raise(TargetClass, "target_class", str(current_user.school_info.grade))
    else:
        raise InsufficientData('type', "university or school")
    return grade


# Contest filter
_filter_fields = ['base_contest_id', 'end_date', 'academic_year', 'composite_type']


def get_contest_filtered(args):
    marshmallow = FilterOlympiadAllRequestSchema().load(args)

    filters = {v: marshmallow[v] for v in _filter_fields if v in marshmallow}

    query = db.with_polymorphic(Contest, [SimpleContest]).query.filter_by(**filters)

    location_id = marshmallow.get('location_id', None)

    if location_id is not None:
        query = query.filter(SimpleContest.locations.any(location_id=location_id))

    target_class_id = marshmallow.get('target_class', None)

    if target_class_id is not None:
        query = query.filter(SimpleContest.target_classes.any(target_class_id=target_class_id))

    offset = marshmallow.get('offset', None)
    limit = marshmallow.get('limit', None)

    query.order_by(SimpleContest.start_date)

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    contest_list = query.all()
    return contest_list

    # Exceptions


class ContestContentAccessDenied(RequestError):
    """
    User has no access to contest
    """

    def __init__(self):
        """
        Create error object
        """
        super(ContestContentAccessDenied, self).__init__(403)

    def get_msg(self) -> str:
        return 'User has no access to this contest'


class ContestIsStillOnReview(RequestError):
    """
    Contest is still on review
    """

    def __init__(self):
        """
        Create error object
        """
        super(ContestIsStillOnReview, self).__init__(403)

    def get_msg(self) -> str:
        return 'Contest is still on review'


def split_line(font, text, width):
    text = text + ' '
    lines = []
    while text:
        index = text.find(' ')
        last_space = None
        while index != -1 and font.getsize(text[:index])[0] <= width:
            last_space = index
            new_index = text[index+1:].find(' ')
            if new_index == -1:
                lines.append(text[:-1])
                return lines
            index = index + new_index + 1
        if last_space is None:
            last_space = index
        lines.append(text[:last_space])
        text = text[last_space + 1:]
    return lines


def put_text_on_image(img_data, x, y, width, text, size, font, spacing, color):
    from PIL import Image, ImageDraw, ImageFont

    text = " ".join(text.strip().split())
    font = ImageFont.truetype(font, size)
    lines = split_line(font, text, width)

    img = Image.open(img_data)
    draw = ImageDraw.Draw(img)

    mid = x + (width / 2)
    multiline = "\n".join(lines)
    draw.multiline_text((mid, y), multiline, color, font, 'ms', spacing, 'center')

    bands = img.getbands()
    if bands == ('R', 'G', 'B', 'A'):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    elif bands != ('R', 'G', 'B'):
        raise TypeError(f'Unknown color encoding: {bands}')

    output = io.BytesIO()
    img.save(output, format='pdf')
    output.seek(0)
    return output


def find_certificate(current_user, current_contest):

    result = UserInContest.query.filter_by(user_id=current_user.id, contest_id=current_contest.contest_id).one_or_none()
    if result is None:
        raise NotFound('UserInContest (user_id, contest_id)', f'({current_user.id}, {current_contest.id})')
    user_status = result.user_status

    certificate_type = current_contest.base_contest.certificate_type
    if certificate_type is None:
        raise InsufficientData('contest', 'certificate')

    certificate = certificate_type.certificates.filter_by(certificate_category=user_status).one_or_none()
    if certificate is None or certificate.certificate_image is None:
        raise InsufficientData('(contest, user_status)', 'certificate')

    return certificate


def get_certificate_for_user(user_info, contest_name, certificate):
    from flask import send_file

    img_data = app.media_to_io(certificate.certificate_image)
    user_name = f'{user_info.second_name} {user_info.first_name} {user_info.middle_name}'
    img = put_text_on_image(img_data, certificate.text_x, certificate.text_y, certificate.text_width, user_name,
                            certificate.text_size, certificate.text_style, certificate.text_spacing,
                            certificate.text_color)
    return send_file(img, mimetype='application/pdf', as_attachment=True,
                     attachment_filename=f'Сертификат_{contest_name}_{user_name}'.replace(" ", "_"))
