from default_config import DefaultConfiguration
from common import OrgMephiApp

from news import module

app = OrgMephiApp('visitor', module, default_config=DefaultConfiguration(), security=False)
app.set_current()
app.prepare()
flask_app = app.app

if __name__ == "__main__":
    app.run()
