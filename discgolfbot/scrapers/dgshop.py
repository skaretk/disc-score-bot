import time
from discs.disc import Disc
from .scraper import Scraper

class DgShop(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'dgshop.no'
        self.url = 'https://www.dgshop.no'

class DiscScraper(DgShop):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://www.dgshop.no/catalogsearch/result/index/?cat=3&q={search}'
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_header_get_beatifulsoup()

        for product in soup.findAll("div", class_="product-item-info"):
            product_item_name = product.find("strong", class_="product name product-item-name")
            if product_item_name is None:
                continue
            item_url = product_item_name.find("a", class_="product-item-link")
            name = item_url.getText().strip().replace("\n", "")
            if self.search.lower() not in name.lower():
                continue
            price = product.find("span", class_="normal-price").getText().replace("\n", "")

            product_photo = product.find("a", class_="product photo product-item-photo")
            url = product_photo["href"]
            product_item_photo = product_photo.find("img", class_="product-image-photo")
            img = product_item_photo["src"]

            disc = Disc()
            disc.name = name
            disc.url = url
            disc.price = price
            disc.img = img
            disc.store = self.name
            self.discs.append(disc)

        self.scraper_time = time.time() - start_time
        print(f'DgShop scraper: {self.scraper_time}')
