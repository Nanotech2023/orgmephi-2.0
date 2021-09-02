from common import OrgMephiModule, OrgMephiArea
from .creator import module as creator_module
from .participant import module as participant_module

module = OrgMephiModule('responses', __package__, access_level=None, marshmallow_api=True, area=OrgMephiArea.both)
module.add_module(creator_module)
module.add_module(participant_module)
