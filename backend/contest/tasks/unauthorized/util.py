from contest.tasks.models import SimpleContest, Contest
from contest.tasks.unauthorized.schemas import FilterOlympiadAllRequestSchema

_filter_fields = ['base_contest_id', 'end_date']


def filter_olympiad_query(args):
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

    query = query.with_polymorphic([SimpleContest]).order_by(SimpleContest.start_date)

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    contest_list = query.all()

    if marshmallow.get('only_count', False):
        return {
                   'count': len(contest_list)
               }, 200
    else:
        return {
                   'contest_list': contest_list,
                   'count': len(contest_list)
               }, 200
