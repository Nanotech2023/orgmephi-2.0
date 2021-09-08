from common import OrgMephiModule, OrgMephiAccessLevel, OrgMephiArea

module = OrgMephiModule('editor', __package__, access_level=OrgMephiAccessLevel.creator,
                        marshmallow_api=True, area=OrgMephiArea.internal)

