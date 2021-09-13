from web import discinstock
from web import sunesport
from web import xxl
from web import discexpress
from web import discconnection
from web import discsport
from web import discmania
from web import rocketdiscs
from web import latitude64
from web import discrepublic

class DiscScrapers():
    def __init__(self, search):
        self.norwegian =     [discinstock.DiscScraper(search),                               
                              sunesport.DiscScraper(search),
                              xxl.DiscScraper(search)]
        self.voec =          [discexpress.DiscScraper(search),
                              discconnection.DiscScraper(search),
                              discsport.DiscScraper(search),
                              discmania.DiscScraper(search),
                              rocketdiscs.DiscScraper(search)]
        self.international = [latitude64.DiscScraper(search),
                              discrepublic.DiscScraper(search)]
