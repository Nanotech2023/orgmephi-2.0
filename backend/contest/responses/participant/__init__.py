from common import OrgMephiModule, OrgMephiAccessLevel

module = OrgMephiModule('participant', __package__, access_level=OrgMephiAccessLevel.participant, 
                        api_file='responses_participant_api.yaml')
