import time
from discs.disc import DiscShop
from .scraper import Scraper

class GuruDiscgolf(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'gurudiscgolf.no'
        self.url = 'https://gurudiscgolf.no/'

class DiscScraper(GuruDiscgolf):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://gurudiscgolf.no/?s={search}&post_type=product&_product_categories=golfdiscer'
        self.discs = []
    
    def scrape(self):
        start_time = time.time()
        soup = self.get_page(1)

        for product in soup.select('li[class*="ast-col-sm-12 ast-article-post astra-woo-hover-zoom"]'):
            product_data = product.find("span", class_="gtm4wp_productdata")
            product_name = product_data['data-gtm4wp_product_name']
            if (self.search.lower() not in product_name.lower()):
                continue
            url = product_data['data-gtm4wp_product_url']
            price = product_data['data-gtm4wp_product_price']
            
            disc = DiscShop()
            disc.name = product_name
            disc.url = url
            disc.price = f'{price},-'
            disc.store = self.name

            img = product.find("img", class_="attachment-woocommerce_thumbnail size-woocommerce_thumbnail")
            if (img is not None):
                disc.img = img['src']

            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'GuruDiscGolf scraper: {self.scraper_time}')
