from contest.default_config import DefaultConfiguration
from common import OrgMephiApp

from contest.tasks.creator import module

app = OrgMephiApp('editor', module, default_config=DefaultConfiguration())
app.set_current()
app.prepare()
flask_app = app.app

if __name__ == "__main__":
    app.run()
