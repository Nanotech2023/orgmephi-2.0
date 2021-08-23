from common import OrgMephiModule, OrgMephiAccessLevel, OrgMephiArea

module = OrgMephiModule('subservice2', __package__, OrgMephiAccessLevel.visitor, marshmallow_api=True,
                        area=OrgMephiArea.both)
