from flask import request
from marshmallow import EXCLUDE

from common import get_current_module
from common.errors import AlreadyExists
from common.media_types import CertificateImage
from common.util import db_add_if_not_exists, db_exists
from contest.tasks.admin.schemas import *
from contest.tasks.model_schemas.certificate import CertificateTypeSchema, CertificateSchema
from contest.tasks.models.certificate import CertificateType, Certificate
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


# Olympiad types


@module.route('/olympiad_type/create', methods=['POST'],
              input_schema=CreateOlympiadTypeRequestTaskAdminSchema, output_schema=OlympiadTypeResponseTaskAdminSchema)
def olympiad_type_create():
    """
    Add olympiad type
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateOlympiadTypeRequestTaskAdminSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: OlympiadTypeResponseTaskAdminSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow
    olympiad_type = values['olympiad_type']

    new_olympiad_type = add_olympiad_type(olympiad_type=olympiad_type)

    db_add_if_not_exists(db.session, OlympiadType, new_olympiad_type, ['olympiad_type'])
    db.session.commit()

    return {
               "olympiad_type_id": new_olympiad_type.olympiad_type_id
           }, 200


@module.route('/olympiad_type/<int:id_olympiad_type>/remove', methods=['POST'])
def olympiad_type_remove(id_olympiad_type):
    """
    Remove olympiad type
    ---
    post:
      parameters:
        - in: path
          description: Id of the olympiad type
          name: id_olympiad_type
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
          description: Olympiad type not found
    """
    current_olympiad = db_get_or_raise(OlympiadType, "olympiad_type_id", str(id_olympiad_type))
    db.session.delete(current_olympiad)
    db.session.commit()

    return {}, 200


# Location


@module.route('/location/create_online', methods=['POST'],
              input_schema=CreateOnlineLocationRequestTaskAdminSchema, output_schema=LocationResponseTaskAdminSchema)
def online_location_create():
    """
    Add new online location
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateOnlineLocationRequestTaskAdminSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: LocationResponseTaskAdminSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow
    url = values['url']

    new_location = add_online_location(db.session,
                                       url=url)
    db.session.commit()

    return {
               "location_id": new_location.location_id
           }, 200


@module.route('/location/create_russia', methods=['POST'],
              input_schema=CreateRussiaLocationRequestTaskAdminSchema, output_schema=LocationResponseTaskAdminSchema)
def location_create_russia():
    """
    Add new location
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateRussiaLocationRequestTaskAdminSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: LocationResponseTaskAdminSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow
    city_name = values['city_name']
    region_name = values['region_name']
    address = values['address']

    new_location = add_russia_location(db.session,
                                       city_name=city_name,
                                       region_name=region_name,
                                       address=address)
    db.session.commit()

    return {
               "location_id": new_location.location_id
           }, 200


@module.route('/location/create_other', methods=['POST'],
              input_schema=CreateOtherLocationRequestTaskAdminSchema, output_schema=LocationResponseTaskAdminSchema)
def location_create_other():
    """
    Add new location
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateOtherLocationRequestTaskAdminSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: LocationResponseTaskAdminSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow
    country_name = values['country_name']
    location_ = values['location']

    new_location = add_other_location(db.session,
                                      country_name=country_name,
                                      location=location_)
    db.session.commit()

    return {
               "location_id": new_location.location_id
           }, 200


@module.route('/location/<int:id_location>/remove', methods=['POST'])
def location_remove(id_location):
    """
    Remove location
    ---
    post:
      parameters:
        - in: path
          description: Id of the location
          name: id_location
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
          description: Olympiad type not found
    """
    current_location = db_get_or_raise(OlympiadLocation, "location_id", str(id_location))
    db.session.delete(current_location)
    db.session.commit()

    return {}, 200


@module.route('/certificate_type', methods=['POST'], output_schema=CertificateTypeSchema)
def add_certificate_type():
    """
    Add certificate type
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CertificateTypeSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: CertificateTypeSchema
    """
    certificate_type = CertificateTypeSchema().load(request.json, session=db.session, partial=False, unknown=EXCLUDE)
    db.session.add(certificate_type)
    db.session.commit()
    return certificate_type, 200


@module.route('/certificate_type/<int:certificate_type_id>', methods=['PATCH'])
def patch_certificate_type(certificate_type_id):
    """
    Patch certificate type
    ---
    patch:
      parameters:
        - in: path
          description: Id of the certificate type
          name: certificate_type_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: CertificateTypeSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '204':
          description: OK
        '404':
          description: Certificate type not found
    """
    certificate_type = db_get_or_raise(CertificateType, 'certificate_type_id', certificate_type_id)
    CertificateTypeSchema(load_instance=True).load(request.json, session=db.session, partial=True, unknown=EXCLUDE,
                                                   instance=certificate_type)
    db.session.commit()
    return {}, 204


@module.route('/certificate_type/<int:certificate_type_id>', methods=['DELETE'])
def delete_certificate_type(certificate_type_id):
    """
    Delete certificate type
    ---
    delete:
      parameters:
        - in: path
          description: Id of the certificate type
          name: certificate_type_id
          required: true
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '204':
          description: OK
        '404':
          description: Certificate type not found
    """
    certificate_type = db_get_or_raise(CertificateType, 'certificate_type_id', certificate_type_id)
    db.session.delete(certificate_type)
    db.session.commit()
    return {}, 204


@module.route('/certificate_type/<int:certificate_type_id>/certificate', methods=['POST'],
              output_schema=CertificateSchema)
def add_certificate(certificate_type_id):
    """
    Add certificate type
    ---
    post:
      parameters:
        - in: path
          description: Id of the certificate type
          name: certificate_type_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: CertificateSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: CertificateSchema
    """
    certificate_type = db_get_or_raise(CertificateType, 'certificate_type_id', certificate_type_id)
    certificate = CertificateSchema().load(request.json, session=db.session, partial=False, unknown=EXCLUDE)
    category = certificate.certificate_category
    exists = db_exists(db.session, Certificate, filters={
        'certificate_type_id': certificate_type_id,
        'certificate_category': category
    })
    if exists:
        raise AlreadyExists(f'Certificate type', category.value)

    try:
        from PIL import ImageFont
        font = ImageFont.truetype(certificate.text_style)
    except OSError:
        raise InsufficientData('Font', certificate.text_style)

    certificate_type.certificates.append(certificate)
    db.session.commit()
    return certificate, 200


@module.route('/certificate/<int:certificate_id>', methods=['PATCH'])
def patch_certificate(certificate_id):
    """
    Patch certificate
    ---
    patch:
      parameters:
        - in: path
          description: Id of the certificate
          name: certificate_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: CertificateSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '204':
          description: OK
        '404':
          description: Certificate not found
    """
    certificate = db_get_or_raise(Certificate, 'certificate_id', certificate_id)
    certificate = CertificateSchema(load_instance=True)\
        .load(request.json, session=db.session, partial=True, unknown=EXCLUDE, instance=certificate)

    category = certificate.certificate_category
    query = Certificate.query.filter_by(certificate_type_id=certificate.certificate_type_id,
                                        certificate_category=category).\
        filter(Certificate.certificate_id != certificate.certificate_id)
    exists = db.session.query(query.exists()).scalar()
    if exists:
        raise AlreadyExists(f'Certificate type', category.value)

    db.session.commit()
    return {}, 204


@module.route('/certificate_type/<int:certificate_id>', methods=['DELETE'])
def delete_certificate(certificate_id):
    """
    Delete certificate
    ---
    delete:
      parameters:
        - in: path
          description: Id of the certificate
          name: certificate_id
          required: true
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '204':
          description: OK
        '404':
          description: Certificate not found
    """
    certificate = db_get_or_raise(Certificate, 'certificate_id', certificate_id)
    db.session.delete(certificate)
    db.session.commit()
    return {}, 204


@module.route('/certificate/<int:certificate_id>/image', methods=['POST'])
def post_certificate_image(certificate_id):
    """
    Post certificate image
    ---
    post:
      parameters:
        - in: path
          description: Id of the certificate
          name: certificate_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          image/png:
            schema:
              type: string
              format: binary
          image/jpeg:
            schema:
              type: string
              format: binary
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '204':
          description: OK
        '404':
          description: Certificate not found
    """
    certificate = db_get_or_raise(Certificate, 'certificate_id', certificate_id)
    app.store_media('CERTIFICATE', certificate, 'certificate_image', CertificateImage)
    db.session.commit()
    return {}, 204


@module.route('/fonts', methods=['GET'], output_schema=FontsResponseTasksAdminSchema)
def get_fonts():
    """
    List available fonts
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: FontsResponseTasksAdminSchema
    """
    import matplotlib.font_manager
    system_fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
    font_names = [font.split('/')[-1].split('.')[0] for font in system_fonts]
    return {'fonts': font_names}, 200


@module.route('/certificate', methods=['GET'])
def get_certificate():
    """
    Get certificate for a user
    ---
    get:
      parameters:
        - in: query
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
        - in: query
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/pdf:
              schema:
                type: string
                format: binary
    """
    args = GetCertificateArgsTasksAdminSchema().load(request.args, partial=False, unknown=EXCLUDE)
    user_id = args['user_id']
    contest_id = args['contest_id']

    current_contest = db_get_or_raise(Contest, "contest_id", contest_id)
    current_user = db_get_or_raise(User, "user_id", user_id)

    certificate = find_certificate(current_user, current_contest)
    return get_certificate_for_user(current_user.user_info, current_contest.name, certificate)


@module.route('/certificate/<int:certificate_id>/test', methods=['GET'])
def test_certificate(certificate_id):
    """
    Test certificate rendering
    ---
    get:
      parameters:
        - in: path
          description: Id of the certificate
          name: certificate_id
          required: true
          schema:
            type: integer
        - in: query
          description: User first name
          name: first_name
          required: false
          schema:
            type: integer
        - in: query
          description: User second name
          name: second_name
          required: false
          schema:
            type: integer
        - in: query
          description: User middle name
          name: middle_name
          required: false
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/pdf:
              schema:
                type: string
                format: binary
    """
    from user.models import UserInfo

    args = TestCertificateArgsTasksAdminSchema().load(request.args, partial=False, unknown=EXCLUDE)
    certificate = db_get_or_raise(Certificate, 'certificate_id', certificate_id)

    test_user = UserInfo(first_name=args['first_name'], second_name=args['second_name'],
                         middle_name=args['middle_name'])

    return get_certificate_for_user(test_user, 'test contest', certificate)
