from common import OrgMephiModule, OrgMephiAccessLevel, OrgMephiArea

module = OrgMephiModule('creator', __package__, access_level=OrgMephiAccessLevel.creator, marshmallow_api=True,
                        area=OrgMephiArea.internal)
