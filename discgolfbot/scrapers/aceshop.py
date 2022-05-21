import time
from discs.disc import DiscShop
from .scraper import Scraper

class AceShop(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'aceshop.no'
        self.url = 'https://aceshop.no'

class DiscScraper(AceShop):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://aceshop.no/search_result?keywords={search}'
        self.discs = []
    
    def scrape(self):
        start_time = time.time()
        soup = self.get_page()   

        for product in soup.findAll("div", class_="product"):

            product_box = product.find("div", class_="product_box_title_row")
            product_box_a = product_box.find("a", class_="title")
            name = product_box_a.getText()
            if self.search.lower() not in name.lower():
                continue
            url = product_box_a["href"]            
            price = product.find("div", class_="price").getText().strip()
            product_item_photo = product.find("img", class_="img-fluid")
            img = product_item_photo["src"]            
            
            disc = DiscShop()
            disc.name = name
            disc.url = url
            disc.price = price
            disc.img = img
            disc.store = self.name
            self.discs.append(disc)

        self.scraper_time = time.time() - start_time
        print(f'Aceshop scraper: {self.scraper_time}')
