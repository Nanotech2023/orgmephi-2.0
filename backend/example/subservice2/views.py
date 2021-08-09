from flask import make_response

from common import get_current_module

module = get_current_module()


@module.route('/hello', methods=['GET'])
def hello():
    from datetime import datetime
    time = datetime.now()
    if 6 <= time.hour < 12:
        msg = 'Good morning'
    elif 12 <= time.hour < 18:
        msg = 'Good afternoon'
    elif 18 <= time.hour < 24:
        msg = 'Good evening'
    else:
        msg = 'ZzZzZ...'
    return make_response({'msg': msg}, 200)
