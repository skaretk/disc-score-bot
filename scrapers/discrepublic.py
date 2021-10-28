import time
import re
from scrapers.scraper import Scraper
from discs.disc import DiscShop

class Discrepublic(Scraper):
    def __init__(self, search):
        super().__init__(search)
        self.url = 'discrepublic.ca'

class DiscScraper(Discrepublic):
    def __init__(self, search):
        super().__init__(search)
        self.url_product = 'https://discrepublic.ca'
        self.search_url = f'https://discrepublic.ca/search?type=product&collection=in-stock&q=*{search}*'
    
    def scrape(self):
        start_time = time.time()
        soup = self.get_page(1)        

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

            disc = DiscShop()
            disc.name = f'{mold} {plastic.getText()}'
            product_title = product.find("div", class_="product-title")                
            title = product_title.find('a', href=True)
            # manufacturer is fetched from an alt string
            img = product.find('img', class_="not-rotation img-responsive front")
            disc.manufacturer = img["alt"].split(" ")[0]
            disc.url = f'{self.url_product}{title["href"]}'

            # If the disc is on sale, there is two prices. Check and use correct
            normal_price = product.find("span", class_="price_sale price_normal")
            if normal_price is None:
                disc.price = product.find("span", class_="price_sale").getText().replace("\n", "")
            else:
                disc.price = normal_price.getText().replace("\n", "")
            disc.store = self.url                

            self.discs.append(disc)
        self.search_time = time.time() - start_time
        print(f'Discrepublic scraper: {self.get_search_time()}')
