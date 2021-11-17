from scrapers import discinstock
from scrapers import sunesport
from scrapers import xxl
from scrapers import discexpress
from scrapers import discconnection
from scrapers import discsport
from scrapers import discmania
from scrapers import rocketdiscs
from scrapers import latitude64
from scrapers import discrepublic
from scrapers import discimport
from scrapers import armspeed

class DiscScrapers():
    def __init__(self, search):
        self.norwegian =     [discinstock.DiscScraper(search),                               
                              sunesport.DiscScraper(search),
                              xxl.DiscScraper(search)]
        self.voec =          [discexpress.DiscScraper(search),
                              discconnection.DiscScraper(search),
                              discsport.DiscScraper(search),
                              discmania.DiscScraper(search),
                              rocketdiscs.DiscScraper(search),
                              discimport.DiscScraper(search),
                              armspeed.DiscScraper(search)]
        self.international = [latitude64.DiscScraper(search),
                              discrepublic.DiscScraper(search)]
