from flask import request

from common import get_current_app, get_current_module, get_current_db

db = get_current_db()
module = get_current_module()
app = get_current_app()
