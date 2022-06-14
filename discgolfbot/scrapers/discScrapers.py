from . import aceshop
from . import armspeed
from . import dgshop
from . import discconnection
from . import discexpress
from . import discimport
from . import discinstock
from . import discmania
from . import discrepublic
from . import discsport
from . import frisbeefeber
from . import krokholdgs
from . import latitude64
from . import rocketdiscs
from . import sunesport
from . import xxl

class DiscScrapers():
    def __init__(self, search):
        self.norwegian =     [aceshop.DiscScraper(search),
                              dgshop.DiscScraper(search),
                              discinstock.DiscScraper(search),
                              frisbeefeber.DiscScraper(search),
                              krokholdgs.DiscScraper(search),
                              sunesport.DiscScraper(search)]
        self.voec =          [discsport.DiscScraper(search),
                              rocketdiscs.DiscScraper(search),
                              discmania.DiscScraper(search),
                              latitude64.DiscScraper(search),
                              discexpress.DiscScraper(search),
                              discconnection.DiscScraper(search),
                              discimport.DiscScraper(search),
                              armspeed.DiscScraper(search)]
        self.international = [discrepublic.DiscScraper(search)]
