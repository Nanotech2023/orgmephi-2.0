from contest.default_config import DefaultConfiguration
from common import OrgMephiApp

from . import module

app = OrgMephiApp('tasks', module, default_config=DefaultConfiguration())
app.set_current()
app.prepare()
flask_app = app.app

if __name__ == "__main__":
    app.run()