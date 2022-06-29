import time
from discs.disc import DiscShop
from .scraper import Scraper

class Fyndisc(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'fyndisc.se'
        self.url = 'https://fyndisc.se'

class DiscScraper(Fyndisc):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://fyndisc.se/search/?lang=NOK&q={search}'
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_header_get_beatifulsoup(headers={'Cookie': 'lang=NOK; localization=NO'})

        products = soup.find('ul', class_="js-product-items")
        if (products is not None):
            for product in products.findAll("li", class_="product-item"):
                product_name = product.find("h3", class_="product-item__heading").getText()
                if self.search.lower() not in product_name.lower():
                    continue

                disc = DiscShop()
                disc.name = product_name
                disc.price = product.find("span", class_="price").getText()

                product_item_img = product.find("div", class_="product-item__img")
                product_item_img_a = product_item_img.find("a", href=True)
                product_url = product_item_img_a["href"]
                disc.url = f'{self.url}{product_url}'

                product_item_image = product_item_img_a.find("img", class_="js-product-item-img")
                if product_item_image is not None:
                    product_image = product_item_image["src"]
                    disc.img = f'{self.url}{product_image}'

                disc.store = self.name
                self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'Fyndisc scraper: {self.scraper_time}')
