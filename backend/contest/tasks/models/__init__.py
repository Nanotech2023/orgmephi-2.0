from .contest import *
from .olympiad import *
from .tasks import *
from .user import *
from .location import *

if __name__ == "__main__":
    get_current_db().create_all()
