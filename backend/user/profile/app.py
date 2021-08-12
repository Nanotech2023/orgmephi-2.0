from user.default_config import DefaultConfiguration
from common import OrgMephiApp

from . import module

app = OrgMephiApp('profile', module, default_config=DefaultConfiguration(), marshmallow_api=True)
app.set_current()
app.prepare()
flask_app = app.app

if __name__ == "__main__":
    app.run()
