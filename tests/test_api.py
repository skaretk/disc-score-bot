import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

import context
from context import apis

def test_discgolfmetrix_courses_list():
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.courses_list()    
    assert response is not None

def test_discgolfmetrix_courses_list_course_name():
    course_name = "Muselunden"
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.courses_list("NO", course_name)
    assert response is not None

def test_discgolfmetrix_course_id():
    course_id = "8752"
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.course(course_id)    
    assert response is not None

def test_discgolfmetrix_course_id_code():
    course_id = "8752"
    code = "0"
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.course(course_id, code)    
    assert response is not None

def test_discgolfmetrix_get_results():
    results_id = "2100955"
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.get_results(results_id)    
    assert response is not None

def test_discgolfmetrix_bagtag():
    bagtag_id = "4" # Norway bagtag
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.bagtag_list(bagtag_id)    
    assert response is not None

def test_discgolfmetrix_my_competitions():
    player_code = "HtDz6uLTsF76bFmCGToVsNe9khDf3sJA" # My Current Player ID
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.my_competitions(player_code)    
    assert response is not None