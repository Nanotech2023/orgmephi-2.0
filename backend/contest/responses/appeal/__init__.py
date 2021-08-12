from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('appeal', __package__, access_level=OrgMephiAccessLevel.admin,
                        api_file='responses_appeal_api.yaml')
