"""Base Scraper for PDGA"""
from disc_score_bot.scrapers.scraper import Scraper

class Pdga(Scraper):
    """Base Scraper for PDGA"""
    def __init__(self):
        super().__init__()
        self.name = 'PDGA'
        self.url = 'https://www.pdga.com/'
