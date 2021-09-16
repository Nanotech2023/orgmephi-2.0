from common.jwt_verify import jwt_get_id
from contest.tasks.models import SimpleContest, Contest
from contest.tasks.unauthorized.schemas import FilterOlympiadAllRequestSchema
from contest.tasks.util import is_user_in_contest

_filter_fields = ['base_contest_id', 'end_date']


def filter_olympiad_query_with_enrolled_flag(args):
    marshmallow = FilterOlympiadAllRequestSchema().load(args)

    filters = {v: marshmallow[v] for v in _filter_fields if v in marshmallow}

    query = Contest.query.filter_by(**filters)

    location_id = marshmallow.get('location_id', None)

    if location_id is not None:
        query = query.filter(SimpleContest.locations.any(location_id=location_id))

    target_class_id = marshmallow.get('target_class', None)

    if target_class_id is not None:
        query = query.filter(SimpleContest.target_classes.any(target_class_id=target_class_id))

    offset = marshmallow.get('offset', None)
    limit = marshmallow.get('limit', None)

    query = query.order_by(SimpleContest.start_date)

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    contest_list = query.all()

    user_id = jwt_get_id()

    contests_with_flags = [{
        'contest': contest,
        'enrolled': is_user_in_contest(user_id, contest)

    } for contest in contest_list]

    if marshmallow.get('only_count', False):
        return {
                   'count': len(contests_with_flags)
               }, 200
    else:
        return {
                   'contest_list': contests_with_flags,
                   'count': len(contests_with_flags)
               }, 200
