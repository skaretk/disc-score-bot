import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))
from context import apis

def test_discinstock_discs_list():
    api = apis.discinstockapi.DiscinstockApi()
    assert api is not None
    response = api.discs()
    assert response is not None

def test_discinstock_discs_search():
    api = apis.discinstockapi.DiscinstockApi()
    assert api is not None
    response = api.discs_search('frisbeebutikken')
    assert response is not None

def test_discinstock_brands():
    api = apis.discinstockapi.DiscinstockApi()
    assert api is not None
    response = api.brands()
    assert response is not None

def test_discinstock_retailers():
    api = apis.discinstockapi.DiscinstockApi()
    assert api is not None
    response = api.retailers()
    assert response is not None
