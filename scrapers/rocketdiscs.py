import time
import re
from bs4 import BeautifulSoup
from scrapers.scraper import Scraper
from discs.disc import DiscShop

class RocketDiscs(Scraper):
    def __init__(self, search):
        super().__init__(search)
        self.url = 'rocketdiscs.com'

class DiscScraper(RocketDiscs):
    def __init__(self, search):
        super().__init__(search)
        self.url_product = 'https://rocketdiscs.com'
        self.search_url = f'https://rocketdiscs.com/Search-Results?search_text={search}'

    def any_products(self, soup):
        if soup.find("div", class_="list-group-item padding0") is None:
            return False
        return True        
        
    def scrape(self):
        start_time = time.time()

        soup_search, driver = self.get_page_and_driver()        

        if (self.any_products(soup_search)) == False:
            driver.close()
            self.search_time = time.time() - start_time
            print(f'RocketDiscs scraper: {self.get_search_time()}')
            return
        
        for product in soup_search.findAll("div", class_="list-group-item padding0"):
            name = product.find("h4", class_="media-heading").getText()
            if re.search(self.search, name, re.IGNORECASE) is None:
                continue

            disc = DiscShop()
            disc.name = name
            meta = product.find("p", class_="meta").getText()
            disc.manufacturer = meta.split("|")[0].replace("\n", "").replace(" ", "")
            #plastic = meta.split("|")[1].lstrip(" ").rstrip(" ")
            url = product.find("a", class_="pull-left", href=True)
            disc.url = f'{self.url_product}{url["href"]}'

            driver_button = driver.find_element_by_class_name("pull-left")
            driver.execute_script("arguments[0].click();", driver_button)        
            driver.refresh()
            soup_product = BeautifulSoup(driver.page_source, "html.parser")
            disc.price = soup_product.find("td", id="ContentPlaceHolder1_lblOurPrice").text
            img = soup_product.find("img", id="ContentPlaceHolder1_discImage")
            if (img is not None):
                disc.img = f'{self.url_product}{img["src"]}'
            disc.store = self.url
            self.discs.append(disc)
            break
            
        driver.close()
        self.search_time = time.time() - start_time
        print(f'RocketDiscs scraper: {self.get_search_time()}')
