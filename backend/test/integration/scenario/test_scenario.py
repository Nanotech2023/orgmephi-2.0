from . import *
from pytest_steps import test_steps
from .steps_init import steps_init
from .steps_register_creator import steps_register_creator
from .steps_create_olympiad_type import steps_create_olympiad_type
from .steps_create_olympiad import steps_create_olympiad
from .steps_create_news import steps_create_news
from .steps_browse_news import steps_browse_news
from .steps_register_participants import steps_register_participants
from .steps_enroll import steps_enroll
from .steps_participate import steps_participate
from .steps_support import steps_support
from .steps_check import steps_check
from .steps_results import steps_results
from .steps_appeal_request import steps_appeal_request
from .steps_view_work import steps_view_work
from .steps_appeal_response import steps_appeal_response


@test_steps(*steps_init, *steps_register_creator, *steps_create_olympiad_type, *steps_create_olympiad,
            *steps_create_news, *steps_browse_news, *steps_register_participants, *steps_enroll, *steps_participate,
            *steps_support, *steps_check, *steps_results, *steps_appeal_request, *steps_view_work,
            *steps_appeal_response)
def test_integration(test_step, steps_data):
    test_step(getattr(steps_data, 'client', None), steps_data)
