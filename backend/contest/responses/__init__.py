from common import OrgMephiModule
from .creator import module as creator_module
from .participant import module as participant_module
from .general import module as general_module

module = OrgMephiModule('responses', __package__, access_level=None)
module.add_module(creator_module)
module.add_module(participant_module)
module.add_module(general_module)
