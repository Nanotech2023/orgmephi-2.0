from sqlalchemy.orm import Query

from common.util import db_get_all
from contest.tasks.models import SimpleContest, BaseContest, ContestTypeEnum
from contest.tasks.unauthorized.schemas import FilterOlympiadAllRequestSchema

_filter_fields = ['base_contest_id', 'end_date']


def filter_olympiad_query(args):
    marshmallow = FilterOlympiadAllRequestSchema().load(args)

    filters = {v: marshmallow[v] for v in _filter_fields if v in marshmallow}

    target_class = marshmallow.get('target_class', None)
    if target_class is not None:
        all_base_contest = db_get_all(BaseContest)
        base_contests: list[BaseContest] = [
            base_contest for base_contest
            in all_base_contest
            if target_class in base_contest.target_classes
        ]
        filters['composite_type'] = ContestTypeEnum.SimpleContest
        query: Query = base_contests[0].child_contests.filter_by(**filters)
        for base_contest in base_contests:
            query = query.union_all(base_contest.child_contests.filter_by(**filters))
    else:
        query = SimpleContest.query.filter_by(**filters)

    location_id = marshmallow.get('location_id', None)

    if location_id is not None:
        query = query.filter(SimpleContest.locations.any(location_id=location_id))

    offset = marshmallow.get('offset', None)
    limit = marshmallow.get('limit', None)

    query = query.order_by(SimpleContest.start_date)

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
