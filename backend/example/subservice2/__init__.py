from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('subservice2', __package__, OrgMephiAccessLevel.visitor, marshmallow_api=True)
