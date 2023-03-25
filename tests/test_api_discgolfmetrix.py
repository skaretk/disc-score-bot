import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

from context import apis

def test_discgolfmetrix_courses_list():
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.courses_list()
    assert response is not None

def test_discgolfmetrix_courses_list_course_name():
    course_name = "Bikkjestykket"
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.courses_list("NO", course_name)
    assert response is not None
    # Fetch and test that we have received the courses
    courses = response.get("courses")
    assert len(courses) != 0

def test_discgolfmetrix_course_id():
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.course(course_id="8752")
    assert response is not None

def test_discgolfmetrix_course_id_code():
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.course(course_id="8752", code="0")
    assert response is not None

def test_discgolfmetrix_get_results():
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.get_results(result_id="2023035")
    assert response is not None

def test_discgolfmetrix_get_results_class():
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.get_results(result_id="2023035", class_="MPO")
    assert response is not None

def test_discgolfmetrix_get_results_group():
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.get_results(result_id="2023035", group="1")
    assert response is not None

def test_discgolfmetrix_bagtag():
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.bagtag_list(bagtag_id="4") # Norway bagtag
    assert response is not None

def test_discgolfmetrix_my_competitions():
    api = apis.discgolfmetrixapi.DiscgolfMetrixApi()
    assert api is not None
    response = api.my_competitions(code="HtDz6uLTsF76bFmCGToVsNe9khDf3sJA") # My Current Player ID
    assert response is not None