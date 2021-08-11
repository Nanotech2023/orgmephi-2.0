from common import OrgMephiModule
from .registration import module as registration_module
from .auth import module as auth_module

module = OrgMephiModule('user', __package__, access_level=None, api_file='user_api.yaml')
module.add_module(registration_module)
module.add_module(auth_module)
