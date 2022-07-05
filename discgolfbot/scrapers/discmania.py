import time
import re
from discs.disc import Disc
from .scraper import Scraper

class Discmania(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'discmania.net'
        self.url = 'https://europe.discmania.net'

class DiscScraper(Discmania):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://europe.discmania.net/search?type=product%2Carticle%2Cpage&q={search}'
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_get_beatifulsoup()

        for product in soup.findAll("div", class_="o-layout__item u-1/1 u-1/2@phab u-1/4@tab"):
            name = product.find("h3", class_= "product__title h4").getText()

            if re.search(self.search, name, re.IGNORECASE) is None: # Gives some false products
                continue
            money = product.find("span", class_="money")
            if (money == None): # Not in stock
                continue

            disc = Disc()
            disc.name = name
            disc.manufacturer = product.find("h4", class_= "product__vendor h6").getText()
            a = product.find("a", class_="product-link", href=True)
            disc.url = f'{self.url}{a["href"]}'
            img = product.find("img", class_="product__img lazyautosizes lazyloaded")
            if (img is not None):
                disc.img = f'https:{img["data-srcset"].split()[8].split("?v=", 1)[0]}' #fetch 540 width image
            disc.price = money.getText()
            disc.store = self.name
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'Discmania scraper: {self.scraper_time}')
