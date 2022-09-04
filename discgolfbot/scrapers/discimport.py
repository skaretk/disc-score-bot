import time
from discs.disc import Disc
from .scraper import Scraper

# DiscImport
class DiscImport(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'discimport.com'
        self.url = 'https://discimport.com'

class DiscScraper(DiscImport):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://discimport.com/?s={search}&post_type=product'
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_header_get_beatifulsoup()

        for product_li in soup.findAll('li', class_='product'):
            if 'outofstock' in product_li['class']:
                continue
            title = product_li.find('h2', class_='woocommerce-loop-product__title').getText()
            if self.search.lower() not in title.lower(): # check false results
                continue
            a = product_li.find('a', href=True)
            price, currency = product_li.find('span', class_='woocommerce-Price-amount').findAll(text=True)
            price = price.strip()
            img_url = product_li.find('img', src=True)['src'] # TODO: this will return a 324px image, get higher res?
            # TODO: scrape flight numbers?
            disc = Disc()
            disc.name = title
            disc.price = f'{price} {currency}'
            disc.url = a['href']
            disc.img = img_url
            disc.store = self.name
            self.discs.append(disc)

        self.scraper_time = time.time() - start_time
        print(f'DiscImport scraper: {self.scraper_time}')
