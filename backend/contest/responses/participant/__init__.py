from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('participant', __package__, access_level=OrgMephiAccessLevel.participant, 
                        marshmallow_api=True)
