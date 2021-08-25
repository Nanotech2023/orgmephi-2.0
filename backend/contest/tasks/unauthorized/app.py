from default_config import DefaultConfiguration
from common import OrgMephiApp

from contest.tasks.unauthorized import module

app = OrgMephiApp('unauthorized', module, default_config=DefaultConfiguration())
app.set_current()
app.prepare()
flask_app = app.app

if __name__ == "__main__":
    app.run()
