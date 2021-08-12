import random

from flask import abort, request, make_response

from common.errors import NotFound, InsufficientData
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_or_raise, db_get_all
from common.jwt_verify import jwt_get_id

from contest.tasks.models import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/variant/<int:variant_num>',
    methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def variant_get(id_olympiad, id_stage, id_contest, variant_num):
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db_get_or_raise(Stage, "stage_id", str(id_stage))
    contest = db_get_or_raise(Contest, "contest_id", str(id_contest))
    variant = contest.variants.filter_by(**{"variant_number": str(variant_num)}).one_or_none()

    if variant is None:
        raise NotFound("variant_number", str(variant_num))

    return make_response(
        variant.serialize(), 200)
