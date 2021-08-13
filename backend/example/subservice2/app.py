from example.default_config import DefaultConfig
from common import OrgMephiApp

from . import module

app = OrgMephiApp('example_subservice2', module, default_config=DefaultConfig())
app.set_current()
app.prepare()
flask_app = app.app

if __name__ == "__main__":
    app.run()
