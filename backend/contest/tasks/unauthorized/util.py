from contest.tasks.unauthorized.schemas import FilterOlympiadAllRequestSchema
from contest.tasks.util import get_contest_filtered


def filter_olympiad_query(args):
    marshmallow = FilterOlympiadAllRequestSchema().load(args)

    contest_list = get_contest_filtered(args)

    if marshmallow.get('only_count', False):
        return {
                   'count': len(contest_list)
               }, 200
    else:
        return {
                   'contest_list': contest_list,
                   'count': len(contest_list)
               }, 200
