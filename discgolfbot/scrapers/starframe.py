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
        soup = self.selenium_get_beatifulsoup(sleep_time=1)

        for product in soup.find_all("div", {"class": "crall-product-item"}):
            disc_name = product.find("div", {"class": "crall-product-name"}).getText()
            if self.search.lower() not in disc_name.lower():
                continue

            product_image = product.find("div", {"class": "crall-product-image"})
            img_fluid = product.find("img", {"class": "img-fluid"})
            div_price = product.find("div", {"class": "crall-price"})
            url = product_image.find('a', href=True)

            disc = Disc()
            disc.name = disc_name.strip()
            disc.url = url["href"]
            disc.price = div_price.getText().strip()
            disc.img = img_fluid["src"]
            disc.store = self.name
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'Starframe scraper: {self.scraper_time}')
