import time
import re
from scrapers.scraper import Scraper
from discs.disc import DiscShop

class Discsport(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'discsport.se'
        self.url = 'https://discsport.se'

class DiscScraper(Discsport):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://discsport.se/shopping/?search_adv=&name={search}&selBrand=0&selCat=1&selType=0&selStatus=0&selMold=0&selDiscType=0&selStability=0&selPlastic=0&selPlasticQuality=0&selColSel=0&selColPrim=0&selCol=0&selWeightInt=0&selWeight=0&sel_speed=0&sel_glide=0&sel_turn=-100&sel_fade=-100&Submit='
        self.discs = []
    
    def scrape(self):
        start_time = time.time()
        soup = self.get_page()        

        products = soup.find('ul', class_="products")
        if (products is not None):
            for product in products.findAll("li"):
                label = product.find("div", class_="upperLeftLabel")
                if label is not None:
                    if label.getText().replace("\n", "") != "NEW":
                        continue # Not in stock / Restock Delayed

                disc = DiscShop()
                a = product.find("h3", class_="shop_item").find('a', href=True)
                disc.name = a.getText().replace("\n", " ").replace("\t", " ")
                disc.url = a["href"]
                manufacturer = re.search(r"]<br/>(.*?)\|", a["title"]).group(1).replace("\xa0", "")
                if (manufacturer is not None):
                    disc.manufacturer = manufacturer
                img = product.find("img", class_="lozad")
                if (img is not None):
                    disc.img = img["data-src"]
                disc.price = product.find("div", class_="text-center").find("p").getText()
                disc.store = self.name
                self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'Discsport scraper: {self.scraper_time}')
