from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('admin', __package__, access_level=OrgMephiAccessLevel.admin,
                        marshmallow_api=True)

