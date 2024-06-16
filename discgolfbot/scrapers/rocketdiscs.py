import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from disc.disc import Disc
from .scraper import Scraper

class RocketDiscs(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'rocketdiscs.com'
        self.url = 'https://rocketdiscs.com'

class DiscScraper(RocketDiscs):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://rocketdiscs.com/Search-Results?search_text={search}'
        self.discs = []

    def any_products(self, soup):
        if soup.find("div", class_="list-group-item padding0") is None:
            return False
        return True

    def scrape(self):
        start_time = time.time()
        soup_search = self.urllib_get_beatifulsoup()
        if self.any_products(soup_search) == False:
            self.scraper_time = time.time() - start_time
            print(f'RocketDiscs scraper: {self.scraper_time}')
            return

        for product in soup_search.findAll("div", class_="list-group-item padding0"):
            name = product.find("h4", class_="media-heading").getText()
            if self.search.lower() not in name.lower(): # Gives some false products
                continue

            disc = Disc()
            disc.name = name
            meta = product.find("p", class_="meta").getText()
            disc.manufacturer = meta.split("|")[0].strip()
            url = product.find("a", class_="pull-left", href=True)
            disc.url = f'{self.url}{url["href"]}'

            with urlopen(disc.url) as sock:
                htmlSource = sock.read()
            soup_product = BeautifulSoup(htmlSource, "html.parser")

            # Todo: Might fail here?
            disc.price = soup_product.find("td", id="ContentPlaceHolder1_lblOurPrice").text
            img = soup_product.find("img", id="ContentPlaceHolder1_discImage")
            if img is not None:
                disc.img = f'{self.url}{img["src"]}'
            disc.store = self.name
            plastics = []
            plastics_div = soup_product.find('div', class_='plastics')
            if plastics_div:
                plastics = [plastic.getText().strip() for plastic in plastics_div.find_all('a')]
            if plastics:
                disc.name += ' [' + ', '.join(plastics) + ']'
            self.discs.append(disc)
            break

        self.scraper_time = time.time() - start_time
        print(f'RocketDiscs scraper: {self.scraper_time}')
