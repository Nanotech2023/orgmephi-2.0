from common import OrgMephiModule, OrgMephiArea
from analytics import module as analytics_module
from contest import module as contest_module
from user import module as user_module
from messages import module as messages_module
from news import module as news_module

module = OrgMephiModule('aggregate', __package__, access_level=None, marshmallow_api=True, area=OrgMephiArea.both)
module.add_module(analytics_module)
module.add_module(contest_module)
module.add_module(user_module)
module.add_module(messages_module)
module.add_module(news_module)
