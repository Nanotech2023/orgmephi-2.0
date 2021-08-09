from common import OrgMephiModule
from .tasks import module as tasks_module
from .responses import module as responses_module

module = OrgMephiModule('contest', __package__, access_level=None)
module.add_module(tasks_module)
module.add_module(responses_module)
