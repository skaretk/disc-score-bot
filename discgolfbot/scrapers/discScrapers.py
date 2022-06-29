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
                              discinstock.DiscScraperApi(search),
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

    @property
    def norwegian_scrapers(self):
        return self.norwegian

    @property
    def voec_scrapers(self):
        scraper_list = self.norwegian
        scraper_list.extend(self.voec)
        return scraper_list

    @property
    def all_scrapers(self):
        scraper_list = self.norwegian
        scraper_list.extend(self.voec)
        scraper_list.extend(self.international)
        return scraper_list
