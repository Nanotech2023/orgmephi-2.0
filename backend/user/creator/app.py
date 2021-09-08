from user.default_config import DefaultConfiguration
from common import OrgMephiApp

from user.creator import module

app = OrgMephiApp('creator', module, default_config=DefaultConfiguration())
app.set_current()
app.prepare()
flask_app = app.app

if __name__ == "__main__":
    app.run()
