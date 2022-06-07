import time
import re
from discs.disc import DiscShop
from .scraper import Scraper
# This site has been added into DiscInStock site

class FrisbeeFeber(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'frisbeefeber.no'
        self.url = 'https://www.frisbeefeber.no'

class DiscScraper(FrisbeeFeber):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://www.frisbeefeber.no/search_result?keywords={search}'
        self.discs = []
    
    def scrape(self):
        start_time = time.time()
        soup = self.urllib_get_beatifulsoup()

        for product in soup.select('li[class*="product-box-id-"]'):
            # In stock ?
            not_in_stock = product.find("div", class_="product not-in-stock-product")
            if (not_in_stock is not None):
                continue
            disc = DiscShop()
            disc.name = product.find("a", class_="title col-md-12").getText()
            # Search engine gives false results, check if the disc name is correct
            if re.search(self.search, disc.name, re.IGNORECASE) is None:
                continue
            div_manufacturer = product.find("div", class_="manufacturer-box")
            alt_manufacturer = div_manufacturer.find("img", alt=True)
            disc.manufacturer = alt_manufacturer['alt']
            disc.price = product.find("div", class_="price col-md-12").getText().replace('\n','').replace('\t', '').strip()
            disc.store = self.name
            url = product.find('a', href=True)
            disc.url = url['href']

            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'FrisbeeFeber scraper: {self.scraper_time}')
