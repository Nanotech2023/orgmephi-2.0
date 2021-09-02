from common import OrgMephiModule, OrgMephiAccessLevel, OrgMephiArea

module = OrgMephiModule('admin', __package__, access_level=OrgMephiAccessLevel.admin,
                        marshmallow_api=True, area=OrgMephiArea.internal)

