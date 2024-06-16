import time
from disc.disc import Disc
from .scraper import Scraper

class Kastmeg(Scraper):
    """kastmeg.no scraper"""
    def __init__(self):
        super().__init__()
        self.name = 'kastmeg.no'
        self.url = 'https://kastmeg.no'

class DiscScraper(Kastmeg):
    """kastmeg.no disc scraper"""
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://kastmeg.no/search?q={search}'
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_get_beatifulsoup()

        for product in soup.findAll("li", {"class" : "grid__item"}):
            card_heading = product.find("h3", {"class" : "card__heading"})
            name = card_heading.getText().strip()
            if self.search.lower() not in name.lower():
                continue

            # Is the disc in stock ?
            in_stock = product.find("span", {"class" : "badge--bottom-left"})
            if in_stock is not None:
                if in_stock.getText() == "Utsolgt":
                    continue

            manufacturer_div = product.find("div", {"class" : "caption-with-letter-spacing"})
            if manufacturer_div is not None:
                manufacturer = manufacturer_div.getText()

            price = product.find("span", {"class" : "price-item--regular"}).getText().strip()

            card_heading_a = card_heading.find("a", {"class" : "full-unstyled-link"})
            url = card_heading_a["href"]

            media = product.find("div", {"class" : "media"})
            media_img = media.find("img", {"class" : "motion-reduce"})

            img = f'https:{media_img["srcset"].replace("{width}", "540").split("?v=", 1)[0]}' # fetch 540x width image

            disc = Disc()
            disc.name = name
            disc.manufacturer = manufacturer if manufacturer_div is not None else ''
            disc.url = f'{self.url}/{url}'
            disc.price = price
            disc.img = img
            disc.store = self.name
            self.discs.append(disc)

        self.scraper_time = time.time() - start_time
        print(f'Kastmeg scraper: {self.scraper_time}')
