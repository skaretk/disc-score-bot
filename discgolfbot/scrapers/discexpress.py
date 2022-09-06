import time
from discs.disc import Disc
from .scraper import Scraper

# Discexpress does not contain disc manufacturer
class DiscExpress(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'discexpress.se'
        self.url = 'https://www.discexpress.se'

class DiscScraper(DiscExpress):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://www.discexpress.se/a/search?type=product&q={search}'
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_header_get_beatifulsoup(headers={'Cookie': 'cart_currency=NOK'})

        for product_item in soup.findAll("div", class_="product-item product-item--vertical 1/3--tablet 1/4--lap-and-up"):
            a = product_item.find('a', class_='product-item__title')
            name = a.getText()

            if self.search.lower() not in name.lower(): # Search engine gives false response
                continue
            disc = Disc()
            disc.name = name
            disc.url = f'{self.url}{a["href"]}'
            img = product_item.find('img', src=True) # find the non-JS image tag
            if (img is not None):
                img_url = f'https:{img["src"]}'
                disc.img = img_url
            
            disc.price = ''.join(product_item.find('span', class_='price').findAll(text=True, recursive=False)).strip()
            disc.store = self.name
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'DiscExpress scraper: {self.scraper_time}')
