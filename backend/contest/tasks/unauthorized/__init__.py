from common import OrgMephiModule, OrgMephiArea, OrgMephiAccessLevel

module = OrgMephiModule('unauthorized', __package__, access_level=OrgMephiAccessLevel.visitor,
                        marshmallow_api=True, area=OrgMephiArea.external)
