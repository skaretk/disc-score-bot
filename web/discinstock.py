import time
from web.scraper import Scraper
from discs.disc import DiscShop

class DiscInStock(Scraper):
    def __init__(self, search):
        super().__init__(search)

class DiscScraper(DiscInStock):
    def __init__(self, search):
        super().__init__(search)
        self.search_url = f'https://www.discinstock.no/?name={search}'
    
    def scrape(self):
        start_time = time.time()
        soup = self.get_page(1)        

        for a in soup.findAll("div", class_="col"):
            disc = DiscShop()
            disc.manufacturer = a.find("h6", class_="text-muted font-monospace h-100").getText()
            disc.name = a.find("span", class_="fs-5").getText()
            img = a.find("img", class_="px-1 pt-1")
            disc.img = img["src"]
            disc.price = a.find("span", class_="flex-shrink-1 display-6 mt-1").getText()
            disc.store = a.find("span", class_="mx-auto").getText()
            link = a.find('a', href=True)
            disc.url = link['href']

            self.discs.append(disc)
        self.search_time = time.time() - start_time
        print(f'DiscInStock scraper: {self.get_search_time()}')