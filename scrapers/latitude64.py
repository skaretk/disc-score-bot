import time
from scrapers.scraper import Scraper
from discs.disc import DiscShop

class Latitude64(Scraper):
    def __init__(self, search):
        super().__init__(search)
        self.url = 'store.latitude64.se'

class DiscScraper(Latitude64):
    def __init__(self, search):
        super().__init__(search)
        self.url_product = 'https://store.latitude64.se/'
        self.search_url = f'https://store.latitude64.se/search?q={search}'
    
    def scrape(self):
        start_time = time.time()
        soup = self.get_page(1)        

        for prodHeader in soup.findAll("div", class_="box product"):
            title =  prodHeader.find("a", class_="title")
            if (title is None):
                continue
            disc = DiscShop()
            disc.name = title.getText()
            disc.url = f'{self.url_product}{title["href"]}'
            disc.manufacturer = prodHeader.find("span", class_="vendor").getText()
            disc.price = prodHeader.find("span", class_="money").getText()
            disc.store = self.url
            self.discs.append(disc)
        self.search_time = time.time() - start_time
        print(f'Latitude64 scraper: {self.get_search_time()}')
