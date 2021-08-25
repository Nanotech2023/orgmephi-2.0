from common import OrgMephiApp
from default_config import DefaultConfiguration
from contest.tasks import module

app = OrgMephiApp('tasks', module, default_config=DefaultConfiguration(), security=True)
app.set_current()
app.prepare()
flask_app = app.app

if __name__ == "__main__":
    app.run()
