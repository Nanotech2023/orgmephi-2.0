from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('profile', __package__, access_level=OrgMephiAccessLevel.participant,
                        api_file='user_profile_api.yaml')
