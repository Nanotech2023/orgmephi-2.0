from common import OrgMephiModule
from .contest_create import module as creator_module
from .admin import module as admin_module
from .participant import module as participant_module

module = OrgMephiModule('tasks', __package__, access_level=None, api_file='tasks_api.yaml')

module.add_module(creator_module)
module.add_module(admin_module)
module.add_module(participant_module)
