import time
from discs.disc import Disc
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
        products_div = soup.find('div', class_='products-grid product-search row product-collection')
        if products_div is not None:
            for product_item_div in products_div.findAll("div", class_="inner product-item"):
                product_title_a = product_item_div.find("a", class_="product-title")
                if product_title_a is None:
                    continue
                disc = Disc()
                disc.name = product_title_a.getText().replace('\n', '')
                disc.url = f'{self.url}{product_title_a["href"]}'
                disc.manufacturer = product_item_div.find('div', class_='product-vendor').getText().replace('\n', '')
                disc.price = product_item_div.find("div", class_="price-box").getText().replace('\n', '')
                disc.store = self.name
                self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'Latitude64 scraper: {self.scraper_time}')
