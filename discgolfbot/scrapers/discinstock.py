from datetime import datetime
import time
from discs.disc import Disc
from .scraper import Scraper
from apis.discinstockapi import DiscinstockApi

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
        soup = self.selenium_get_beatifulsoup(1)

        for a in soup.findAll("div", class_="col"):
            disc = Disc()
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

class DiscScraperApi(DiscInStock):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.discs = []

    def scrape(self):
        discinstock_api = DiscinstockApi()
        start_time = time.time()
        discs_json = discinstock_api.discs()
        for disc_json in discs_json:
            if self.search.lower() in disc_json["name"].lower():
                disc = Disc()
                disc.name = disc_json["name"]
                disc.img = disc_json["image"]
                disc.url = disc_json["url"]
                disc.manufacturer = disc_json["brand"]
                disc.price = f'{disc_json["price"]},-'
                disc.store = disc_json["retailer"]
                self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'DiscInStockApi scraper: {self.scraper_time}')

class DiscNewsScraperApi(DiscInStock):
    def __init__(self):
        super().__init__()
        self.discs = []

    def sort_discs(self):
        self.discs.sort(key=lambda disc: disc.update, reverse=True)

    def scrape(self):
        discinstock_api = DiscinstockApi()
        start_time = time.time()
        discs_json = discinstock_api.discs()
        for disc_json in discs_json:
            # Only insert discs from last week
            date_updated = datetime.fromisoformat(disc_json["last_updated"]).replace(tzinfo=None)
            time_delta = datetime.now() - date_updated
            if time_delta.days > 7:
                continue

            disc = Disc()
            disc.name = disc_json["name"]
            disc.img = disc_json["image"]
            disc.url = disc_json["url"]
            disc.manufacturer = disc_json["brand"]
            disc.price = f'{disc_json["price"]},-'
            disc.store = disc_json["retailer"]
            disc.update = date_updated
            self.discs.append(disc)
        self.sort_discs()

        self.scraper_time = time.time() - start_time
        print(f'DiscScraperNewsApi scraper: {self.scraper_time}')