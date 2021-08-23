from common import OrgMephiModule, OrgMephiAccessLevel, OrgMephiArea

module = OrgMephiModule('profile', __package__, access_level=OrgMephiAccessLevel.participant, marshmallow_api=True,
                        area=OrgMephiArea.external)
