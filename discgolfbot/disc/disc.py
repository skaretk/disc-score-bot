import urllib.parse

class Disc():
    """Disc class with all properties"""
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
        """Disc flight characteristics"""
        return f'{self.speed}/{self.glide}/{self.turn}/{self.fade}'

    @property
    def img(self):
        """Disc image"""
        return self._img

    @img.setter
    def img(self, i):
        self._img = urllib.parse.quote(i, safe='?:/=&+')
