from common import OrgMephiModule, OrgMephiArea
from .participant import module as participant_module
from .creator import module as creator_module
from .admin import module as admin_module

module = OrgMephiModule('messages', __package__, access_level=None, marshmallow_api=True, area=OrgMephiArea.both)
module.add_module(participant_module)
module.add_module(creator_module)
module.add_module(admin_module)
