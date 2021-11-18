from . import discinstock
from . import sunesport
from . import xxl
from . import discexpress
from . import discconnection
from . import discsport
from . import discmania
from . import rocketdiscs
from . import latitude64
from . import discrepublic
from . import discimport
from . import armspeed


class DiscScrapers():
    def __init__(self, search):
        self.norwegian =     [discinstock.DiscScraper(search),                               
                              sunesport.DiscScraper(search),
                              xxl.DiscScraper(search)]
        self.voec =          [discsport.DiscScraper(search),
                              rocketdiscs.DiscScraper(search),
                              discmania.DiscScraper(search),
                              latitude64.DiscScraper(search),
                              discexpress.DiscScraper(search),
                              discconnection.DiscScraper(search),
                              discimport.DiscScraper(search),
                              armspeed.DiscScraper(search)]
        self.international = [discrepublic.DiscScraper(search)]
