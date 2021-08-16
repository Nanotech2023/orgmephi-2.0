from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('creator', __package__, access_level=OrgMephiAccessLevel.creator,
                        api_file='responses_creator_api.yaml')
