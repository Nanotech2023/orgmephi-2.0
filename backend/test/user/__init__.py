from .. import *


test_user_info = {
    "document": {
        "code": "123-456",
        "document_type": "RFPassport",
        "issue_date": "2021-09-02",
        "issuer": "string",
        "number": "123456",
        "series": "4520"
    },
    "dwelling": {
        "city": "test",
        "country": "native",
        "region": "test",
        "rural": True
    },
    "gender": "Male",
    "limitations": {
        "hearing": True,
        "movement": True,
        "sight": True
    },
    "phone": "8 (800) 555 35 35",
    "place_of_birth": "string"
}


test_university_info = {
    "citizenship": "native",
    "city": "test",
    "grade": 1,
    "region": "test",
    "university": {
        "country": "native",
        "university": "test"
    }
}


test_school_info = {
    "grade": 1,
    "location": {
        "city": "test",
        "country": "native",
        "region": "test",
        "rural": True
    },
    "name": "string",
    "number": 0,
    "school_type": "School"
}