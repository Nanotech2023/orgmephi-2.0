from flask import request

from common import get_current_module
from common.errors import AlreadyExists
from common.util import send_pdf
from contest.responses.util import get_user_in_contest_work
from contest.tasks.control_users.schemas import *
from contest.tasks.util import *
from user.models import UserTypeEnum, SchoolInfo

db = get_current_db()
module = get_current_module()
app = get_current_app()


# Users


@module.route('/contest/<int:id_contest>/add_user', methods=['POST'],
              input_schema=UpdateUserInContestRequestTaskControlUsersSchema)
def add_user_to_contest(id_contest):
    """
    Add user to contest
    ---
    post:
      parameters:
        - in: path
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateUserInContestRequestTaskControlUsersSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow
    user_ids = values['users_id']
    show_results_to_user = values['show_results_to_user']
    location_id = values.get('location_id', None)

    if location_id is not None:
        db_get_or_raise(OlympiadLocation, "location_id", location_id)

    current_contest = get_contest_if_possible(id_contest)
    current_base_contest = get_base_contest(current_contest)
    target_classes = current_base_contest.target_classes

    for user_id in user_ids:
        current_user: User = db_get_or_raise(User, "id", user_id)
        if is_user_in_contest(user_id, current_contest):
            raise AlreadyExists('user_id', user_id)

        if current_user.type == UserTypeEnum.university:
            unfilled = current_user.student_info.unfilled()
            if len(unfilled) > 0:
                raise InsufficientData('user.student_info', str(unfilled))
            grade = TargetClassEnum("student")
        elif current_user.type == UserTypeEnum.school:
            school_info: SchoolInfo = current_user.school_info
            unfilled = school_info.unfilled()
            if len(unfilled) > 0:
                raise InsufficientData('user.school_info', str(unfilled))
            grade = TargetClassEnum(str(school_info.grade))
        else:
            raise InsufficientData('type', "university or school")

        if grade not in target_classes:
            raise InsufficientData('base_contest_id', "current grade of user")

        current_contest.users.append(UserInContest(user_id=user_id,
                                                   show_results_to_user=show_results_to_user,
                                                   location_id=location_id,
                                                   variant_id=generate_variant(id_contest, user_id),
                                                   user_status=UserStatusEnum.Participant))

    db.session.commit()
    return {}, 200


@module.route('/contest/<int:id_contest>/remove_user', methods=['POST'],
              input_schema=UpdateUserInContestRequestTaskControlUsersSchema)
def remove_user_from_contest(id_contest):
    """
    Remove user from contest
    ---
    post:
      parameters:
        - in: path
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateUserInContestRequestTaskControlUsersSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow
    user_ids = values['users_id']

    current_contest = get_contest_if_possible(id_contest)

    for user_id in user_ids:
        current_user = current_contest.users.filter_by(**{"user_id": str(user_id)}).one_or_none()
        if current_user is None:
            raise InsufficientData('user_id', user_id)
        db.session.delete(current_user)

    db.session.commit()

    return {}, 200


@module.route('/contest/<int:id_contest>/change_location', methods=['POST'],
              input_schema=ChangeUsersLocationInContestRequestTaskControlUsersSchema)
def change_user_location(id_contest):
    """
    Change users location
    ---
    post:
      parameters:
        - in: path
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: ChangeUsersLocationInContestRequestTaskControlUsersSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow
    user_ids = values['users_id']

    location_id = values.get('location_id', None)

    if location_id is not None:
        db_get_or_raise(OlympiadLocation, "location_id", location_id)

    current_contest = get_contest_if_possible(id_contest)

    for user_id in user_ids:
        current_user = current_contest.users.filter_by(**{"user_id": str(user_id)}).one_or_none()
        if current_user is None:
            raise InsufficientData('user_id', user_id)
        current_user.location_id = location_id
        db.session.delete(current_user)

    db.session.commit()

    return {}, 200


@module.route(
    '/contest/<int:id_contest>/user/all',
    methods=['GET'], output_schema=UsersResponseTaskControlUsersSchema)
def users_all(id_contest):
    """
    Get all users
    ---
    get:
      parameters:
        - in: path
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UsersResponseTaskControlUsersSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    current_contest = get_contest_if_possible(id_contest)
    return {
               "user_list": current_contest.users.all()
           }, 200


@module.route(
    'contest/<int:id_contest>/user/<int:id_user>/certificate',
    methods=['GET'])
def users_certificate(id_contest, id_user):
    """
    Get certificate
    ---
    get:
      parameters:
        - in: path
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the user
          name: id_user
          required: true
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/pdf:
              schema:
                type: string
                format: binary
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    current_contest = get_contest_if_possible(id_contest)
    current_user = db_get_or_raise(User, 'id', id_user)

    if not is_user_in_contest(id_user, current_contest):
        raise InsufficientData('user_id', id_user)

    unfilled = current_user.unfilled()
    if len(unfilled) > 0:
        raise InsufficientData('user', str(unfilled))

    mark = get_user_in_contest_work(id_user, id_contest).mark
    user_status = db_get_or_raise(UserInContest, 'user_id', id_user).user_status

    return send_pdf('user_certificate.html', u=user, mark=mark, user_status=user_status,
                    back=current_contest)
