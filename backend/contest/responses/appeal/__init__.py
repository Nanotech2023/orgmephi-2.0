from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('appeal', __package__, access_level=None,   # TODO Access level
                        api_file='responses_appeal_api.yaml')
