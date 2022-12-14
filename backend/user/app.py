from default_config import DefaultConfiguration
from common import OrgMephiApp

from user import module

app = OrgMephiApp('user', module, default_config=DefaultConfiguration(), security=True)
app.set_current()
app.prepare()
flask_app = app.app

if __name__ == "__main__":
    app.run()
