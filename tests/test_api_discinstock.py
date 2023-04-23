import sys
from pathlib import Path
from context import apis
from apis.discinstockapi import DiscinstockApi
sys.path.insert(0, str(Path().cwd()))

def test_discinstock_discs_list():
    api = DiscinstockApi()
    assert api is not None
    response = api.discs()
    assert response is not None

def test_discinstock_discs_search():
    api = DiscinstockApi()
    assert api is not None
    response = api.discs_search('frisbeebutikken')
    assert response is not None

def test_discinstock_brands():
    api = DiscinstockApi()
    assert api is not None
    response = api.brands()
    assert response is not None

def test_discinstock_retailers():
    api = DiscinstockApi()
    assert api is not None
    response = api.retailers()
    assert response is not None
