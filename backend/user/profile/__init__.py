from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('profile', __package__, access_level=OrgMephiAccessLevel.participant, marshmallow_api=True)
