from common import OrgMephiModule, OrgMephiAccessLevel, OrgMephiArea

module = OrgMephiModule('participant', __package__, access_level=OrgMephiAccessLevel.participant, 
                        marshmallow_api=True, area=OrgMephiArea.external)
