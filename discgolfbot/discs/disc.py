import urllib.parse

class Disc():
    def __init__(self):
        self.name = ''
        self.manufacturer = ''
        self.speed = ''
        self.glide = ''
        self.turn = ''
        self.fade = ''

class DiscShop(Disc):
    def __init__(self):
        super().__init__()
        self.price = ''
        self.store = ''
        self.url = ''
        self._img = ''
    
    @property
    def img(self):
        return self._img
    
    @img.setter
    def img(self, i):
        self._img = urllib.parse.quote(i, safe='?:/=&+')
    
    def __str__(self):
        return f'name: {self.name}\n'\
               f'manufacturer: {self.manufacturer}\n'\
               f'price: {self.price}\n'\
               f'store: {self.store}\n'\
               f'url: {self.url}\n'

class DiscFlight(Disc):
    def __init__(self):
        super().__init__()
        self.flight_url = ''
    
    def __str__(self):
        return f'name: {self.name}\n'\
               f'manufacturer: {self.manufacturer}\n'\
               f'speed: {self.speed}\n'\
               f'glide: {self.glide}\n'\
               f'turn: {self.turn}\n'\
               f'fade: {self.fade}\n'\
               f'flight_url: {self.flight_url}\n'

class DiscBag(Disc):
    def __init__(self):
        super().__init__()
        self.url = ''
        self.info = ''
    
    def __str__(self):
        return f'{self.name}'
    
    def flight(self):
            return f'{self.speed}/{self.glide}/{self.turn}/{self.fade}'

class PdgaApprovedDisc(Disc):
    def __init__(self):
        super().__init__()
        self.url = ''
        self.manufacturer_url = ''
        self.approved_date = ''
    
    def __eq__(self, other):
        if self.name.lower() == other.name.lower() and self.manufacturer.lower() == other.manufacturer.lower() and self.approved_date.lower() == other.approved_date.lower() and self.url.lower() == other.url.lower():
            return True
        return False
