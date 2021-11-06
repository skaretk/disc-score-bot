import time
import re
from scrapers.scraper import Scraper
from discs.disc import DiscShop

# Armspeed
class ArmSpeed(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'armspeed.se'
        self.url = 'https://armspeed.se'

# Armspeed does not contain manufacturer
class DiscScraper(ArmSpeed):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://armspeed.se/shop/search?s={search}'
        self.discs = []
        self.currency = "SEK"
    
    def scrape(self):
        start_time = time.time()
        soup = self.get_page()

        for product in soup.findAll("div", class_="col-md-4 col-6 product"):
            # Check if product is in stock

            text = product.find('a', class_="color-text-base")
            product_text = re.split(r'(^[^\d]+)', text.getText())[1:][0].rstrip(" ")
            if re.search(self.search, product_text, re.IGNORECASE) is None: # Check false results
                continue

            url = text['href']
            price = product["data-s-price"]

            disc = DiscShop()
            disc.name = product_text
            disc.price = f'{price} {self.currency}'
            disc.url = f'{self.url}{url}'
            disc.store = self.name
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'DiscImport scraper: {self.scraper_time}')
