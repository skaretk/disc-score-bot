import time
import re
from web.scraper import Scraper
from discs.disc import DiscShop

class Discmania(Scraper):
    def __init__(self, search):
        super().__init__(search)
        self.url = 'discmania.net'

class DiscScraper(Discmania):
    def __init__(self, search):
        super().__init__(search)
        self.url_product = 'https://europe.discmania.net'
        self.search_url = f'https://europe.discmania.net/search?type=product%2Carticle%2Cpage&q={search}'
    
    def scrape(self):
        start_time = time.time()
        soup = self.get_page()        

        for product in soup.findAll("div", class_="o-layout__item u-1/1 u-1/2@phab u-1/4@tab"):
            name = product.find("h3", class_= "product__title h4").getText()

            if re.search(self.search, name, re.IGNORECASE) is None: # Gives some false products
                continue

            disc = DiscShop()
            disc.name = name
            disc.manufacturer = product.find("h4", class_= "product__vendor h6").getText()
            a = product.find("a", class_="product-link", href=True)
            disc.url = f'{self.url_product}{a["href"]}'
            disc.price = product.find("span", class_="money").getText()
            disc.store = self.url
            self.discs.append(disc)
        self.search_time = time.time() - start_time
        print(f'Discmania scraper: {self.get_search_time()}')