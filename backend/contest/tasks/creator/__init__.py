from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('creator', __package__, access_level=OrgMephiAccessLevel.creator,
                        marshmallow_api=True)

