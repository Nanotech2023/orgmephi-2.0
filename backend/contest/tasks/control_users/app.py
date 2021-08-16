from contest.tasks.default_config import DefaultConfiguration
from common import OrgMephiApp

from . import module

app = OrgMephiApp('control_users', module, default_config=DefaultConfiguration())
app.set_current()
app.prepare()
flask_app = app.app

if __name__ == "__main__":
    app.run()
