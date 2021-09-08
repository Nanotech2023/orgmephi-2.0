from common import OrgMephiModule, OrgMephiAccessLevel, OrgMephiArea

module = OrgMephiModule('visitor', __package__, access_level=OrgMephiAccessLevel.visitor, marshmallow_api=True,
                        area=OrgMephiArea.external)
