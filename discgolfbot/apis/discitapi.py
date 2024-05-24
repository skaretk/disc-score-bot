import html
import json
import requests
from discs import disc

class DiscitApi():
    """Disc Golf Discs API - https://github.com/cdleveille/discit-api"""
    def __init__(self):
        self.name = 'Disc Golf Discs'
        self.url = 'https://github.com/cdleveille/discit-api'
        self.api_url = 'https://discit-api.fly.dev/disc?'

    def get_disc(self, id_=None, name=None, brand=None, category=None, speed=None, glide=None, turn=None, fade=None, stability=None):
        """Return list of discs. - https://discgolfmetrix.com/?u=rule&ID=49

        Input parameters:
        1. id - Unique identifier of the disc
        2. name - Name of the disc: Aviar, Buzz, Crank SS, etc.
        3. brand - Brand of the disc: Innova, Discraft, Dynamic Discs, etc.
        4. category - Distance Driver, Hybrid Driver, Control Driver, Midrange, Putter
        5. speed - The relative rate at which the disc can travel through the air: 1 to 15
        6. glide - The relative ability of the disc to maintain loft during its flight: 1 to 7
        7. turn - The tendency of the disc to turn over or bank to the right (for RHBH throws) at the start of its flight: +1 to -5
        8. fade - The tendency of the disc to hook left (for RHBH throws) at the end of its flight: 0 to 5
        9. stability - Stable, Overstable, Very Overstable, Understable, Very Understable
        """
        params = {}
        if id_ is not None:
            params["id"] = id_
        if name is not None:
            params["name"] = name
        if brand is not None:
            params['brand'] = brand
        if category is not None:
            params['category'] = category
        if speed is not None:
            params['speed'] = speed
        if glide is not None:
            params['glide'] = glide
        if turn is not None:
            params['turn'] = turn
        if fade is not None:
            params['fade'] = fade
        if stability is not None:
            params['stability'] = stability

        if bool(params) is False:
            return None

        response = requests.get(self.api_url, params=params, timeout=10)
        if response and response.status_code == 200:
            json_list = json.loads(html.unescape(response.text))
            disc_list = []
            for json_disc in json_list:
                disc_list.append(DiscitDisc(json.dumps(json_disc)))
            return disc_list
        return None

class DiscitDisc(disc.Disc):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
        if hasattr(self, 'brand'):
            self.manufacturer = self.brand
        if hasattr(self, 'link'):
            self.url = self.link
        if hasattr(self, 'pic'):
            self.img = self.pic
