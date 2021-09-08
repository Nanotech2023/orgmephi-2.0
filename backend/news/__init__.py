from common import OrgMephiModule, OrgMephiArea
from .visitor import module as visitor_module
from .creator import module as creator_module
from .admin import module as admin_module

module = OrgMephiModule('news', __package__, access_level=None, marshmallow_api=True, area=OrgMephiArea.both)
module.add_module(visitor_module)
module.add_module(creator_module)
module.add_module(admin_module)
