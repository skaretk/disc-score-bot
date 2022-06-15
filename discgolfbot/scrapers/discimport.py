import time
import re
from discs.disc import DiscShop
from .scraper import Scraper

# DiscImport
class DiscImport(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'discimport.dk'
        self.url = 'https://discimport.dk'

class DiscScraper(DiscImport):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://discimport.dk/search?search={search}'
        self.discs = []
    
    def scrape(self):
        start_time = time.time()
        soup = self.urllib_get_beatifulsoup()

        for product_list in soup.findAll("div", class_="product-teaser-inner"):
            # Check if product is in stock
            in_stock = product_list.find("span", class_="product-teaser-availability instock")
            if in_stock is None:
                continue

            a = product_list.find('a', href=True)

            title = product_list.find("div", class_="product-teaser-title").getText()
            if re.search(self.search, title, re.IGNORECASE) is None: # Check false results
                continue

            currency = product_list.find("span", class_="product-teaser-currency").getText() 
            price = product_list.find("span", class_="product-teaser-price").getText()

            disc = DiscShop()
            disc.name = title
            disc.price = f'{price} {currency}'
            disc.manufacturer = product_list.find("div", class_="product-teaser-brand").getText()
            disc.url = a['href']
            disc.store = self.name
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'DiscImport scraper: {self.scraper_time}')
