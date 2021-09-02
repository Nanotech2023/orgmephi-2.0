from user.default_config import DefaultConfiguration
from common import OrgMephiApp

from user.registration import module

app = OrgMephiApp('registration', module, default_config=DefaultConfiguration(), security=True)
app.set_current()
app.prepare()
flask_app = app.app

if __name__ == "__main__":
    app.run()
