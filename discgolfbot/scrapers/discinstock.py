import time
from discs.disc import DiscShop
from .scraper import Scraper

class DiscInStock(Scraper):
    def __init__(self):
        super().__init__()

class DiscScraper(DiscInStock):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://www.discinstock.no/?name={search}'
        self.discs = []
    
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
        self.scraper_time = time.time() - start_time
        print(f'DiscInStock scraper: {self.scraper_time}')
