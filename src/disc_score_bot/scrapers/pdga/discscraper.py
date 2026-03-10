"""Scraper for PDGA Approved Discs"""
import time
import logging

from disc_score_bot.disc.pdgaapproveddisc import PdgaApprovedDisc
from .pdga import Pdga

logger = logging.getLogger(__name__)

class DiscScraper(Pdga):
    """Scraper for PDGA Approved Discs"""
    def __init__(self):
        super().__init__()
        self.scrape_url = f'{self.url}technical-standards/equipment-certification/discs'
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_header_get_beatifulsoup()

        manufacturers = soup.find_all("td", class_="views-field views-field-field-equipment-manuf-ref")
        disc_models = soup.find_all("td", class_="views-field views-field-title")
        approved_dates = soup.find_all("td", class_="views-field views-field-field-equipment-approve-date")

        for idx, disc_model in enumerate(disc_models):
            approved_disc = PdgaApprovedDisc()
            # Fetch Manufacturer
            manufacturer = manufacturers[idx].getText()
            approved_disc.manufacturer = manufacturer.replace("\n", "").strip()
            # Fetch Disc Model
            disc_name = disc_model.getText()
            approved_disc.name = disc_name.replace("\n", "").strip()
            # Fetch Approved Date
            approved_date = approved_dates[idx].getText()
            approved_disc.approved_date = approved_date.replace("\n", "").strip()
            # Fetch link
            a = disc_model.find('a', href=True)
            url = f'{self.url}{a["href"]}'
            approved_disc.url = url
            # Append
            self.discs.append(approved_disc)

        self.scraper_time = time.time() - start_time
        logger.info('PDGA scraper: %s', self.scraper_time)
