import time
from disc.disc import Disc
from .scraper import Scraper

class Krokholdgs(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'krokholdgs.no'
        self.url = 'https://www.krokholdgs.no'

class DiscScraper(Krokholdgs):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://www.krokholdgs.no/search_result?keywords={search}'
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.selenium_get_beatifulsoup(2)

        for product in soup.findAll("div", {"class" : ["crall-product-item", "crall-in-stock"]}):
            product_meta = product.find("div", class_="crall-product-name")
            a = product_meta.find('a', href=True)
            product_name = a.getText()
            if self.search.lower() not in product_name.lower():
                continue
            url = a['href']
            price = product.find("span", {"class" : "crall-price"}).getText()
            img_item = product.find("img", class_="img-fluid")
            img = img_item["src"]

            disc = Disc()
            disc.name = product_name
            disc.url = url
            disc.price = price
            disc.img = img
            disc.store = self.name
            self.discs.append(disc)

        self.scraper_time = time.time() - start_time
        print(f'KrokholDgs scraper: {self.scraper_time}')
