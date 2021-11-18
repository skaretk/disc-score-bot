import time
import re
from discs.disc import DiscShop
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
        driver = self.get_driver()
        # add cookie in order to get price in NOK
        driver.add_cookie({"name": "cart_currency", "value": "NOK"})
        driver.refresh()
        soup = self.get_page_from_driver(driver)
        driver.close()

        for grid_item in soup.findAll("div", class_="grid-item search-result large--one-fifth medium--one-third small--one-half"):
            name = grid_item.find("p").getText()
            if re.search(self.search, name, re.IGNORECASE) is None: # Search engine gives false response
                continue

            disc = DiscShop()
            disc.name = name
            a = grid_item.find('a', href=True)
            disc.url = f'{self.url}{a["href"]}'
            img = grid_item.find("img", class_="no-js lazyautosizes lazyloaded")
            if (img is not None):
                disc.img = f'https:{img["data-srcset"].split()[8].split("?v=", 1)[0]}' #fetch 540 width image

            for hidden_item in grid_item.findAll("span", class_="visually-hidden"):
                if re.search("kr", hidden_item.getText(), re.IGNORECASE):
                    disc.price = hidden_item.getText()                 
            disc.store = self.name
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'DiscExpress scraper: {self.scraper_time}')
