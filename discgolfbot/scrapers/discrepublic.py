import time
from disc.disc import Disc
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
            product_name = f'{mold} {plastic.getText()}'
            if self.search.lower() not in product_name.lower(): # Gives some false products
                continue

            div_product_title = product.find("div", class_="product-title")
            a_title = div_product_title.find('a', href=True)
            img = product.find('img', class_="not-rotation img-responsive front")
            span_normal_price = product.find("span", class_="price_sale price_normal")

            disc = Disc()
            disc.name = product_name
            disc.manufacturer = img["alt"].split(" ")[0]
            disc.url = f'{self.url}{a_title["href"]}'
            # If the disc is on sale, there is two prices. Check and use correct
            if span_normal_price is None:
                disc.price = product.find("span", class_="price_sale").getText().replace("\n", "")
            else:
                disc.price = span_normal_price.getText().replace("\n", "")
            disc.img = f'https:{img["src"].split("?v=", 1)[0]}'
            disc.store = self.name
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'Discrepublic scraper: {self.scraper_time}')
