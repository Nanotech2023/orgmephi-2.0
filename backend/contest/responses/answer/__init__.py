from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('answer', __package__, access_level=OrgMephiAccessLevel.admin,
                        api_file='responses_answer_api.yaml')
