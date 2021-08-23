from common import OrgMephiModule, OrgMephiAccessLevel, OrgMephiArea
from .subservice1 import module as sub1module
from .subservice2 import module as sub2module

module = OrgMephiModule('example', __package__, OrgMephiAccessLevel.visitor, area=OrgMephiArea.both)
module.add_module(sub1module)
module.add_module(sub2module)
