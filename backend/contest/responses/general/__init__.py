from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('general', __package__, access_level=OrgMephiAccessLevel.participant,
                        api_file='responses_general_api.yaml')
