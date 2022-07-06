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
        div_products = soup.find('div', class_='products-grid product-search row product-collection')
        if div_products is not None:
            for div_product_item in div_products.findAll("div", class_="inner product-item"):
                a_product_title = div_product_item.find("a", class_="product-title")
                if a_product_title is None:
                    continue
                picture = div_product_item.find("source")

                disc = Disc()
                disc.name = a_product_title.getText().replace('\n', '')
                disc.url = f'{self.url}{a_product_title["href"]}'
                disc.manufacturer = div_product_item.find('div', class_='product-vendor').getText().replace('\n', '')
                disc.price = div_product_item.find("div", class_="price-box").getText().replace('\n', '').replace(",00 kr", ",-")
                disc.img = f'https:{picture["data-srcset"].split("?v=", 1)[0]}'
                disc.store = self.name
                self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'Latitude64 scraper: {self.scraper_time}')
