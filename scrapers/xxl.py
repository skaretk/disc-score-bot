import time
import re
from scrapers.scraper import Scraper
from discs.disc import DiscShop

class Xxl(Scraper):
    def __init__(self, search):
        super().__init__(search)
        self.url = 'xxl.no'

class DiscScraper(Xxl):
    def __init__(self, search):
        super().__init__(search.replace(" ", "+"))
        self.product_url = 'https://www.xxl.no'
        self.search_url = f'https://www.xxl.no/search?query={self.search}&sort=relevance&Frisbeegolffilters_string_mv=Driver&Frisbeegolffilters_string_mv=Putter&Frisbeegolffilters_string_mv=Mid+range+frisbee'
    
    def scrape(self):
        start_time = time.time()
        soup = self.get_page(1)        

        contain_discs = False

        for filter in soup.findAll("div", class_="MuiAccordionSummary-content jss11 Mui-expanded jss12"):
            if "Frisbeegolf" in filter.getText():
                contain_discs = True

        if (contain_discs == False):
            return

        product_list = soup.find("ul", class_="product-list product-list--multiline")
        for product in product_list.findAll("li"):                
            product_info = product.find("div", class_="product-card__info-wrapper")
            name = product_info.find("p").getText().split(", ")[0]
            # Must check since xxl.no returns false results
            if re.search(self.search, name, re.IGNORECASE) is None:
                continue
            disc = DiscShop()
            disc.name = product_info.find("p").getText().split(", ")[0]
            disc.manufacturer = product_info.find("h3").getText()
            product_price = product.find("div", class_="product-card__price-wrapper")                
            disc.price = product_price.find("p").getText()
            a = product.find('a', href=True)
            disc.url = f'{self.product_url}{a["href"]}'
            disc.store = self.url
            self.discs.append(disc)
        self.search_time = time.time() - start_time
        print(f'XXL scraper: {self.get_search_time()}')
