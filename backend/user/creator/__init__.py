from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('creator', __package__, access_level=OrgMephiAccessLevel.creator,
                        api_file='user_creator_api.yaml')
