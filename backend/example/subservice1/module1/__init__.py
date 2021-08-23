from common import OrgMephiModule, OrgMephiAccessLevel, OrgMephiArea

module = OrgMephiModule('module1', __package__, OrgMephiAccessLevel.visitor,
                        api_file='example_subservice1_module1.yaml', area=OrgMephiArea.both)
