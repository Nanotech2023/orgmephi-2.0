from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('status', __package__, access_level=None,   # TODO Access level
                        api_file='responses_status_api.yaml')
