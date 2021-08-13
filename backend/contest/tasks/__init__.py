from common import OrgMephiModule
from .creator import module as creator_module
from .admin import module as admin_module
from .participant import module as participant_module
from .unauthorized import module as unauthorized_module

module = OrgMephiModule('tasks', __package__, access_level=None)

module.add_module(creator_module)
module.add_module(admin_module)
module.add_module(participant_module)
module.add_module(unauthorized_module)
