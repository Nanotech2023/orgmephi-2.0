from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('admin', __package__, access_level=OrgMephiAccessLevel.admin,
                        api_file='user_admin_api.yaml')
