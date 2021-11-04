import time
import re
from scrapers.scraper import Scraper
from discs.disc import DiscShop

# Sune Sport does not contain disc manufacturer
class SuneSport(Scraper):
    def __init__(self, search):
        super().__init__(search)
        self.name = 'sunesport.no'
        self.url = 'https://sunesport.no'

class DiscScraper(SuneSport):
    def __init__(self, search):
        super().__init__(search)
        self.scrape_url = f'https://sunesport.no/product/search.html?search={search}&category_id=268&sub_category=true'
    
    def scrape(self):
        start_time = time.time()
        soup = self.get_page()        

        for product in soup.findAll("div", class_="product-thumb"):
            if (product.find("span", class_="stock-status").getText() == "Utsolgt"):
                continue

            disc = DiscShop()
            caption = product.find("div", class_="caption")
            h4 = caption.find("h4")
            a = h4.find('a', href=True)
            disc.name = a.getText()
            disc.url = a["href"]
            disc.price = re.search(r" (.*?)Ekskl.", caption.find("p", class_="price").getText()).group(1)
            disc.store = self.name
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'SuneSport scraper: {self.scraper_time}')
