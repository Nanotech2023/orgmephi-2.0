from common import OrgMephiModule, OrgMephiArea
from .registration import module as registration_module
from .auth import module as auth_module
from .profile import module as profile_module
from .admin import module as admin_module
from .creator import module as creator_module

module = OrgMephiModule('user', __package__, access_level=None, marshmallow_api=True, area=OrgMephiArea.both)
module.add_module(registration_module)
module.add_module(auth_module)
module.add_module(profile_module)
module.add_module(admin_module)
module.add_module(creator_module)
