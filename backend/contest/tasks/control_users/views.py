from flask import abort, request, make_response

from common import get_current_app, get_current_module
from common.errors import AlreadyExists
from contest.tasks.control_users.schemas import UpdateUserInRequestCreatorSchema, UserCertificateSchema, \
    UsersResponseSchema
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


# Users


@module.route('/contest/<int:id_contest>/add_user', methods=['POST'],
              input_schema=UpdateUserInRequestCreatorSchema)
def add_user_to_contest(id_contest):
    """
    Add user to contest
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateOlympiadTypeRequestAdminSchema
      parameters:
        - in: path
          description: Id of the contest
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
        '400':
          description: Bad request
        '409':
          description: User already in use
    """

    values = request.marshmallow
    user_ids = values['users_id']

    contest = get_contest_if_possible(id_contest)

    for user_id in user_ids:
        if is_user_in_contest(user_id, contest):
            raise AlreadyExists('user_id', user_id)

        contest.users.append(UserInContest(user_id=user_id,
                                           variant_id=generate_variant(id_contest, user_id),
                                           user_status=UserStatusEnum.Participant))

    db.session.commit()
    return {}, 200


@module.route('/contest/<int:id_contest>/remove_user', methods=['POST'],
              input_schema=UpdateUserInRequestCreatorSchema)
def remove_user_from_contest(id_contest):
    """
    Remove user from contest
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateOlympiadTypeRequestAdminSchema
      parameters:
        - in: path
          description: Id of the contest
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
        '400':
          description: Bad request
        '409':
          description: User already in use
        '404':
          description: User not found
    """

    values = request.marshmallow
    user_ids = values['users_id']

    contest = get_contest_if_possible(id_contest)

    for user_id in user_ids:
        user = contest.users.filter_by(**{"user_id": str(user_id)}).one_or_none()
        if user is None:
            raise InsufficientData('user_id', user_id)
        db.session.delete(user)

    db.session.commit()

    return {}, 200


@module.route(
    '/contest/<int:id_contest>/user/all',
    methods=['GET'], input_schema=UsersResponseSchema)
def users_all(id_contest):
    """
    Get all users
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: UsersResponseSchema
      parameters:
        - in: path
          description: Id of the contest
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
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: User not found
    """

    contest = get_contest_if_possible(id_contest)
    return {
               "user_list": contest.users.all()
           }, 200


@module.route(
    'contest/<int:id_contest>/user/<int:id_user>/certificate',
    methods=['GET'], input_schema=UserCertificateSchema)
def users_certificate(id_contest, id_user):
    """
    Get user certificate
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: UserCertificateSchema
      parameters:
        - in: path
          description: Id of the contest
          name: id_contest
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
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
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: User not found
    """
    # contest = get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest)
    # certificate = None

    abort(502)
