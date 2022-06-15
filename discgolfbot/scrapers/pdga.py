import time
from discs.disc import PdgaApprovedDisc
from .scraper import Scraper

class Pdga(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'PDGA Approved Disc Golf Discs'
        self.url = 'https://www.pdga.com/'

class DiscScraper(Pdga):
    def __init__(self):
        super().__init__()
        self.scrape_url = f'https://www.pdga.com/technical-standards/equipment-certification/discs'
        self.discs = []
    
    def scrape(self):
        start_time = time.time()
        soup = self.urllib_header_get_beatifulsoup()

        manufacturers = soup.findAll("td", class_="views-field views-field-field-equipment-manuf-ref")
        disc_models = soup.findAll("td", class_="views-field views-field-title")
        approved_dates = soup.findAll("td", class_="views-field views-field-field-equipment-approve-date")

        for idx, disc_model in enumerate(disc_models):
            approved_disc = PdgaApprovedDisc()
            # Fetch Manufacturer
            manufacturer = manufacturers[idx].getText()
            approved_disc.manufacturer = manufacturer.replace("\n", "").lstrip().rstrip()
            # Fetch Disc Model
            disc_model = disc_models[idx].getText()
            approved_disc.name = disc_model.replace("\n", "").lstrip().rstrip()
            # Fetch Approved Date
            approved_date = approved_dates[idx].getText()
            approved_disc.approved_date = approved_date.replace("\n", "").lstrip().rstrip()
            # Fetch link
            a = disc_models[idx].find('a', href=True)
            url = f'{self.url}{a["href"]}'
            approved_disc.url = url
            # Append
            self.discs.append(approved_disc)

        self.scraper_time = time.time() - start_time
        print(f'PDGA scraper: {self.scraper_time}')
