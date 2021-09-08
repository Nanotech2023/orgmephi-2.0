import os

from aggregate.default_config import DefaultConfiguration
from common import OrgMephiApp, OrgMephiModule

from aggregate import module

API_DIR = 'generated_api'


def _dump_one(mod, path):
    api = mod.get_api()
    if api is not None:
        with open(f'{path}/api.yaml', 'w') as f:
            f.write(api)


def _dump_api(mod: OrgMephiModule, path):
    _dump_one(mod, path)
    for submod in mod.modules:
        subdir = f'{path}/{submod.name}'
        os.makedirs(subdir, exist_ok=True)
        _dump_api(submod, subdir)


app = OrgMephiApp('dump_api', module, default_config=DefaultConfiguration(), security=True)
app.config['ENV'] = 'development'
app.set_current()
app.prepare()

if __name__ == "__main__":
    os.makedirs(API_DIR, exist_ok=True)
    _dump_api(app.top_module, API_DIR)
