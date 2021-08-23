from common import OrgMephiApp
from contest.default_config import DefaultConfiguration

from contest.tasks.participant import module

app = OrgMephiApp('participant', module, default_config=DefaultConfiguration())
app.set_current()
app.prepare()
flask_app = app.app

if __name__ == "__main__":
    app.run()
