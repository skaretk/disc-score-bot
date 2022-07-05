import urllib.parse

class Disc():
    def __init__(self):
        self.name = ''
        self.manufacturer = ''
        self.speed = ''
        self.glide = ''
        self.turn = ''
        self.fade = ''
        self.url = ''
        self.img = ''
        self.price = ''
        self.store = ''
        self.info = ''

    def __str__(self):
        return self.name

    @property
    def flight(self):
        return f'{self.speed}/{self.glide}/{self.turn}/{self.fade}'

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, i):
        self._img = urllib.parse.quote(i, safe='?:/=&+')

class PdgaApprovedDisc(Disc):
    def __init__(self):
        super().__init__()
        self.manufacturer_url = ''
        self.approved_date = ''

    def __eq__(self, other):
        if self.name.lower() == other.name.lower() and self.manufacturer.lower() == other.manufacturer.lower() and self.approved_date.lower() == other.approved_date.lower() and self.url.lower() == other.url.lower():
            return True
        return False
