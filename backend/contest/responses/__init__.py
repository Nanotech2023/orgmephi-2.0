from common import OrgMephiModule
from .answer import module as answer_module
from .status import module as status_module
from .appeal import module as appeal_module

module = OrgMephiModule('responses', __package__, access_level=None)
module.add_module(answer_module)
module.add_module(status_module)
module.add_module(appeal_module)
