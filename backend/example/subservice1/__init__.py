from common import OrgMephiModule, OrgMephiAccessLevel
from .module1 import module as module1
from .module2 import module as module2

module = OrgMephiModule('subservice1', __package__, OrgMephiAccessLevel.visitor)
module.add_module(module1)
module.add_module(module2)
