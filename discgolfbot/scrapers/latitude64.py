import time
from discs.disc import DiscShop
from .scraper import Scraper

class Latitude64(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'store.latitude64.se'
        self.url = 'https://store.latitude64.se'

class DiscScraper(Latitude64):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://store.latitude64.se/search?type=product&q={search}'
        self.discs = []
    
    def scrape(self):
        start_time = time.time()
        soup = self.urllib_get_beatifulsoup()
        productsDiv = soup.find('div', class_='products-grid product-search row product-collection')
        for prodHeader in productsDiv.findAll("div", class_="inner product-item"):
            title = prodHeader.find("a", class_="product-title")
            if title is None:
                continue
            disc = DiscShop()
            disc.name = title.getText().replace('\n', '')
            disc.url = f'{self.url}{title["href"]}'
            disc.manufacturer = prodHeader.find('div', class_='product-vendor').getText().replace('\n', '')
            disc.price = prodHeader.find("div", class_="price-box").getText().replace('\n', '')
            disc.store = self.name
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'Latitude64 scraper: {self.scraper_time}')
