from .reference import *
from .personal import *
from .auth import *
from .university import *
from .school import *
from .location import *
from .document import *

if __name__ == "__main__":
    get_current_db().create_all()
