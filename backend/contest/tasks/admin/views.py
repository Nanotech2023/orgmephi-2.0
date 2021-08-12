import random

from flask import abort
from common.errors import NotFound
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_or_raise
from common.jwt_verify import jwt_get_id

from contest.tasks.models import *

db = get_current_db()
module = get_current_module()
app = get_current_app()
