from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('control_users', __package__, access_level=OrgMephiAccessLevel.creator,
                        api_file='task_control_users_api.yaml')

