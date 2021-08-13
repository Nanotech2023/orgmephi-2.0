from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('unauthorized', __package__, access_level=None,
                        api_file='task_unauthorized_api.yaml')
