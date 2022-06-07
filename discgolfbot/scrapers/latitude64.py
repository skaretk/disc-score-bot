import time
from discs.disc import DiscShop
from .scraper import Scraper

class Latitude64(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'store.latitude64.se'
        self.url = 'https://store.latitude64.se/'

class DiscScraper(Latitude64):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://store.latitude64.se/search?q={search}'
        self.discs = []
    
    def scrape(self):
        start_time = time.time()
        soup = self.get_page(1)

        for prodHeader in soup.findAll("div", class_="box product"):
            title =  prodHeader.find("a", class_="title")
            if (title is None):
                continue
            disc = DiscShop()
            disc.name = title.getText()
            disc.url = f'{self.url}{title["href"]}'
            disc.manufacturer = prodHeader.find("span", class_="vendor").getText()
            disc.price = prodHeader.find("span", class_="money").getText()
            disc.store = self.name
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'Latitude64 scraper: {self.scraper_time}')
