from common import OrgMephiModule, OrgMephiArea
from analytics import module as analytics_module
from contest import module as contest_module
from user import module as user_module

module = OrgMephiModule('aggregate', __package__, access_level=None, marshmallow_api=True, area=OrgMephiArea.both)
module.add_module(analytics_module)
module.add_module(contest_module)
module.add_module(user_module)
