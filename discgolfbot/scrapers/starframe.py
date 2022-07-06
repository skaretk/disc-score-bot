import time
from discs.disc import Disc
from .scraper import Scraper

class Starframe(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'starframe.no'
        self.url = 'https://starframe.no'

class DiscScraper(Starframe):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://www.starframe.no/search_result?keywords={search}'
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_get_beatifulsoup()

        for product in soup.findAll("div", class_="product"):
            disc_name = product.find("a", class_="title").getText()
            if (self.search.lower() not in disc_name.lower()):
                continue

            a_product_url = product.find("a", class_="__product_url")
            img_fluid = a_product_url.find("img", class_="img-fluid")
            p_manufacturer = product.find("p", class_="manufacturers")
            div_price = product.find("div", class_="price")

            disc = Disc()
            disc.name = disc_name
            disc.manufacturer = p_manufacturer["data-manufacturer"]
            disc.url = a_product_url["href"]
            disc.price = div_price.getText().strip()
            disc.img = img_fluid["src"]
            disc.store = self.name
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'Starframe scraper: {self.scraper_time}')
