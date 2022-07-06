import re
import time
from discs.disc import Disc
from .scraper import Scraper

# Sune Sport does not contain disc manufacturer
class SuneSport(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'sunesport.no'
        self.url = 'https://sunesport.no'

class DiscScraper(SuneSport):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://sunesport.no/product/search.html?search={search}&category_id=268&sub_category=true'
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_get_beatifulsoup()

        for product in soup.findAll("div", class_="product-thumb"):
            if (product.find("span", class_="stock-status").getText() == "Utsolgt"):
                continue
            div_caption = product.find("div", class_="caption")
            div_caption_a = div_caption.find('a', href=True)
            div_image = product.find("div", class_="image")

            disc = Disc()
            disc.name = div_caption_a.getText()
            disc.url = div_caption_a["href"]
            disc.price = re.search(r" (.*?)Ekskl.", div_caption.find("p", class_="price").getText()).group(1).strip().replace("Kr ", "").replace(",00", ",-")
            disc.img = div_image.find("img", class_="img-responsive")["src"]
            disc.store = self.name
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'SuneSport scraper: {self.scraper_time}')
