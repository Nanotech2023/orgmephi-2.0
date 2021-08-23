from common import OrgMephiModule, OrgMephiArea

module = OrgMephiModule('auth', __package__, access_level=None, marshmallow_api=True, area=OrgMephiArea.external)
