import pytest
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from tests.testapp import db


@pytest.fixture(scope='function')
def flask_init(request):
    print()
    db.create_all()

    # print(db.engine.table_names())
    yield db
    db.close_all_sessions()
