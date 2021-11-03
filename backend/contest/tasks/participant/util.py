from common.jwt_verify import jwt_get_id
from contest.tasks.unauthorized.schemas import FilterOlympiadAllRequestSchema
from contest.tasks.util import is_user_in_contest, get_contest_filtered


def filter_olympiad_query_with_enrolled_flag(args):
    marshmallow = FilterOlympiadAllRequestSchema().load(args)

    contest_list = get_contest_filtered(args)

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
