import time
import re
from discs.disc import Disc
from .scraper import Scraper

class Discrepublic(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'discrepublic.ca'
        self.url = 'https://discrepublic.ca'

class DiscScraper(Discrepublic):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://discrepublic.ca/search?type=product&collection=in-stock&q=*{search}*'
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_header_get_beatifulsoup(headers={'Cookie': 'cart_currency=NOK; localization=NO'})

        # Check if the disc is sold out
        for product in soup.findAll("div", class_="product-item-wrapper col-sm-2"):
            if product.find("span", class_="sold_out"):
                continue

            # mold contain the disc name, must check this field
            mold = product.find("span", class_="mold").getText()
            plastic = product.find("span", class_="plastic")
            # Is the product a disc?
            if plastic is None:
                continue
            if re.search(self.search, f'{mold} {plastic.getText()}', re.IGNORECASE) is None:
                continue

            disc = Disc()
            disc.name = f'{mold} {plastic.getText()}'
            product_title = product.find("div", class_="product-title")
            title = product_title.find('a', href=True)
            # manufacturer is fetched from an alt string
            img = product.find('img', class_="not-rotation img-responsive front")
            disc.manufacturer = img["alt"].split(" ")[0]
            disc.url = f'{self.url}{title["href"]}'

            # If the disc is on sale, there is two prices. Check and use correct
            normal_price = product.find("span", class_="price_sale price_normal")
            if normal_price is None:
                disc.price = product.find("span", class_="price_sale").getText().replace("\n", "")
            else:
                disc.price = normal_price.getText().replace("\n", "")
            disc.store = self.name

            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'Discrepublic scraper: {self.scraper_time}')
