import sys
from pathlib import Path
from context import apis
from apis.discitapi import DiscitApi
sys.path.insert(0, str(Path().cwd()))

def test_discit_get_disc_id():
    api = DiscitApi()
    assert api is not None
    response = api.get_disc(id_='89bd794c-d3e0-507b-bedd-ae9d623017ea') # firebird
    assert response is not None

def test_discit_get_disc_name():
    api = DiscitApi()
    assert api is not None
    response = api.get_disc(name='firebird')
    assert response is not None

def test_discit_get_disc_brand():
    api = DiscitApi()
    assert api is not None
    response = api.get_disc(brand='innova')
    assert response is not None

def test_discit_get_disc_category():
    api = DiscitApi()
    assert api is not None
    response = api.get_disc(category='Distance Driver')
    assert response is not None
    response = api.get_disc(category='Hybrid Driver')
    assert response is not None
    response = api.get_disc(category='Control Driver')
    assert response is not None
    response = api.get_disc(category='Midrange')
    assert response is not None
    response = api.get_disc(category='Putter')
    assert response is not None

def test_discit_get_disc_speed():
    api = DiscitApi()
    assert api is not None
    response = api.get_disc(speed='0') # too low
    assert response is None
    response = api.get_disc(speed='1') # minimum
    assert response is not None
    response = api.get_disc(speed='15') # max
    assert response is not None
    response = api.get_disc(speed='16') # too high
    assert response is  None

def test_discit_get_disc_glide():
    api = DiscitApi()
    assert api is not None
    response = api.get_disc(glide='0') # too low
    assert response is None
    response = api.get_disc(glide='1') # minimum
    assert response is not None
    response = api.get_disc(glide='7') # max
    assert response is not None
    response = api.get_disc(glide='8') # too high
    assert response is None

def test_discit_get_disc_turn():
    api = DiscitApi()
    assert api is not None
    response = api.get_disc(turn='-6') # too low
    assert response is None
    response = api.get_disc(turn='-5') # minimun
    assert response is not None
    response = api.get_disc(turn='1') # max
    assert response is not None
    response = api.get_disc(turn='2') # too high
    assert response is None

def test_discit_get_disc_fade():
    api = DiscitApi()
    assert api is not None
    response = api.get_disc(fade='-1') # too low
    assert response is None
    response = api.get_disc(fade='0') # minimum
    assert response is not None
    response = api.get_disc(fade='5') # max
    assert response is not None
    response = api.get_disc(fade='6') # too high
    assert response is None

def test_discit_get_disc_stability():
    api = DiscitApi()
    assert api is not None
    response = api.get_disc(stability='rofl')
    assert response is None
    response = api.get_disc(stability='Stable')
    assert response is not None
    response = api.get_disc(stability='Overstable')
    assert response is not None
    response = api.get_disc(stability='Very Overstable')
    assert response is not None
    response = api.get_disc(stability='Understable')
    assert response is not None
    response = api.get_disc(stability='Very Understable')
    assert response is not None

def test_discit_get_disc_multiple_param():
    api = DiscitApi()
    assert api is not None
    response = api.get_disc(speed='1', stability='Overstable')
    assert response is not None
    response = api.get_disc(speed='11', stability='Understable')
    assert response is not None

def test_discit_get_disc_no_params():
    api = DiscitApi()
    assert api is not None
    response = api.get_disc()
    assert response is None
