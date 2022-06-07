import time
from discs.disc import DiscFlight
from .scraper import Scraper

class MarshallStreet(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'marshallstreetdiscgolf.com'
        self.url = 'https://www.marshallstreetdiscgolf.com'

class DiscFlightScraper(MarshallStreet):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://www.marshallstreetdiscgolf.com/flightguide'
        self.discs = []
        self.icon_url= f'https://www.marshallstreetdiscgolf.com/wp-content/uploads/2017/12/cropped-favicon-1-32x32.png'

    def scrape(self):
        start_time = time.time()
        soup = self.get_page(1)
        for disc_item in soup.findAll("div", class_="flex-grid-item disc-item"):
            if (disc_item.getText().lower() == self.search.lower()):
                disc = DiscFlight()
                disc.name = disc_item.getText()
                disc.manufacturer = disc_item['data-brand']
                disc.flight_url = disc_item['data-pic']
                disc.speed = disc_item['data-speed']
                disc.glide = disc_item['data-glide']
                disc.turn = disc_item['data-turn']
                disc.fade = disc_item['data-fade']
                self.discs.append(disc)
                print(f'MarshallStreetFlight scraper: {time.time() - start_time}')
                return
        for putter in soup.findAll("div", class_="putter-child pc-entry"):
            putter_name = putter['data-putter']
            if (putter_name.lower() == self.search.lower()):
                disc = DiscFlight()
                disc.name = putter_name
                disc.manufacturer = putter['data-brand']
                disc.flight_url = putter['data-image']
                disc.speed = putter['data-speed']
                disc.glide = putter['data-glide']
                disc.turn = putter['data-turn']
                disc.fade = putter['data-fade']
                self.discs.append(disc)
                print(f'MarshallStreetFlight scraper: {time.time() - start_time}')
                return
        self.scraper_time = time.time() - start_time
        print(f'MarshallStreetFlight scraper: {self.scraper_time}')
