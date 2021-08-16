from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('admin', __package__, access_level=OrgMephiAccessLevel.admin,
                        api_file='task_admin_api.yaml')

