import json
from .disc import Disc

class DiscitDisc(Disc):
    """DiscitDisc, specific for discit api"""
    def __init__(self, j):
        super().__init__()
        self.__dict__ = json.loads(j)
        if hasattr(self, 'brand'):
            self.manufacturer = self.brand
        if hasattr(self, 'link'):
            self.url = self.link
        if hasattr(self, 'pic'):
            self.img = self.pic
