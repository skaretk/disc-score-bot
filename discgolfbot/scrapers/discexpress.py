import time
from discs.disc import Disc
from .scraper import Scraper

# Discexpress does not contain disc manufacturer
class DiscExpress(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'discexpress.se'
        self.url = 'https://www.discexpress.se'

class DiscScraper(DiscExpress):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://www.discexpress.se/a/search?type=product&q={search}'
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_header_get_beatifulsoup(headers={'Cookie': 'cart_currency=NOK'})

        for grid_item in soup.findAll("div", class_="grid-item search-result large--one-fifth medium--one-third small--one-half"):
            name = grid_item.find("p").getText()

            if self.search.lower() not in name.lower(): # Search engine gives false response
                continue

            disc = Disc()
            disc.name = name
            a = grid_item.find('a', href=True)
            disc.url = f'{self.url}{a["href"]}'
            img = grid_item.find("img", class_="no-js")
            if (img is not None):
                img_url = f'https:{img["data-src"].replace("{width}", "540").split("?v=", 1)[0]}' # fetch 540x width image
                disc.img = img_url

            for hidden_item in grid_item.findAll("span", class_="visually-hidden"):
                if "kr" in hidden_item.getText().lower():
                    disc.price = hidden_item.getText()
            disc.store = self.name
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'DiscExpress scraper: {self.scraper_time}')
