
class Disc():
    def __init__(self):
        self.name = ''
        self.manufacturer = ''

class DiscShop(Disc):
    def __init__(self):
        super().__init__()
        self.price = ''
        self.store = ''
        self.url = ''
        self.img = ''
    
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
        self.speed = ''
        self.glide = ''
        self.turn = ''
        self.fade = ''
    
    def __str__(self):
        return f'name: {self.name}\n'\
               f'manufacturer: {self.manufacturer}\n'\
               f'speed: {self.speed}\n'\
               f'glide: {self.glide}\n'\
               f'turn: {self.turn}\n'\
               f'fade: {self.fade}\n'\
               f'flight_url: {self.flight_url}\n'               
