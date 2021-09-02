from common import OrgMephiModule, OrgMephiAccessLevel, OrgMephiArea

module = OrgMephiModule('module2', __package__, OrgMephiAccessLevel.visitor,
                        api_file='example_subservice1_module2.yaml', area=OrgMephiArea.both)
