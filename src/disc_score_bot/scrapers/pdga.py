import logging
import time
import urllib.parse
from datetime import datetime

from dataclasses import dataclass, field
from disc_score_bot.disc.pdgaapproveddisc import PdgaApprovedDisc
from .scraper import Scraper

logger = logging.getLogger(__name__)

class Pdga(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'PDGA Approved Disc Golf Discs'
        self.url = 'https://www.pdga.com/'

class DiscScraper(Pdga):
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

@dataclass
class PdgaPlayerData:
    pdga_number: str
    current_rating: int = 0
    rating_change: int = 0
    location: str = ''
    membership_status: str = ''
    official_status: str = ''
    career_events: int = 0
    upcoming_events: list = field(default_factory=list)
    portrait_url: str = ''
    player_name: str = ''

    @property
    def dictionary(self):
        """Returns a dictionary"""
        return {
            "Current Rating": self.current_rating,
            "Career Events": self.career_events,
            "Location": self.location,
            "Membership Status": self.membership_status,
            "Official Status": self.official_status,
            "PDGA Number": self.pdga_number,
            "Ratings Change": self.rating_change,
            "Upcoming Events": self.upcoming_events,
        }

class PdgaEvent():
    def __init__(self, url_host:str, url_path:str, title:str, date_start:str, date_from_to:str) -> None:
        self.event_url = urllib.parse.urljoin(base=url_host, url=url_path)
        self.title = title
        self.date_start = date_start
        self.date_from_to = date_from_to
        self._on_init()

    def _on_init(self):
        if self.date_start is None:
            return
        try:
            parsed = datetime.strptime(self.date_start, "%a, %b %d, %Y")
            self.date_start = parsed.strftime("%a, %b %d, %Y")
        except ValueError:
           pass  # date_start is in an unrecognised format, leave as-is

    def __repr__(self) -> str:
        return f'{self.date_start}: [{self.title}]({self.event_url})'

class PlayerProfileScraper(Pdga):
    def __init__(self, pdga_number):
        super().__init__()
        self.name = "PDGA Player Profile"
        self.scrape_url = f'{self.url}player/{pdga_number}'
        self.player_data = PdgaPlayerData(pdga_number=pdga_number)

    def scrape(self):
        start_time = time.time()

        # headers
        headers = {
            "Host": "www.pdga.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "no,en;q=0.7,en-US;q=0.3",
            "Accept-Encoding": "*",
        }
        self.soup = self.urllib_header_get_beatifulsoup(headers=headers)

        # find the location data of the player
        loc_obj = self.soup.find_all('li', class_='location')
        self.player_data.location = loc_obj[0].a.text
        # find the membership status of the player
        membership_obj = self.soup.find_all('li', class_='membership-status')
        self.player_data.membership_status = membership_obj[0].text.split(": ")[-1].strip()
        # find the rules official status of the player
        self.find_official_data()

        # retrieve the player current rating
        self.find_current_rating()

        # find the rating difference gain
        self.find_rating_difference_gain()

        # try to find player portrait data (url and player name)
        player_portrait_data = self.get_player_portrait_data()

        if player_portrait_data:
            # assign the player name from the portrait data
            self.player_data.player_name = player_portrait_data['alt'].split(self.player_data.pdga_number)[0].strip()
        else:
            # assign the player name from the meta tag
            self.find_player_name()
            if self.player_data.portrait_url is None and self.player_data.player_name:
                self.get_player_portrait_data(search_key="'s picture")

        # parse players upcoming event and assemble a string worthy of discord-embeds :)
        self.get_player_upcoming_events_data()

        # find the past events data
        self.get_singles_event_history()

        # print the chore
        self.scraper_time = time.time() - start_time
        logger.info('PDGA PlayerProfileScraper scraper: %s', self.scraper_time)

    def find_player_name(self):
        player_name_metadata = self.soup.find(name="meta", property="og:title")
        if 'content' in player_name_metadata.attrs:
            self.player_data.player_name = player_name_metadata.attrs['content'].split("#")[0].rstrip()

    def find_current_rating(self):
        current_rating_data = self.soup.find('li', class_='current-rating')
        if current_rating_data is None:
            self.player_data.current_rating = 'n/a'
            return
        self.player_data.current_rating = current_rating_data.text.split(": ")[-1].strip()


    def find_rating_difference_gain(self):
        rating_diff_data = self.soup.find_all(name='a', property='rating-difference gain')
        if len(rating_diff_data) == 0:
            self.player_data.rating_change = 'n/a'
            return
        self.player_data.rating_change = rating_diff_data[0].text

    def get_singles_event_history(self):
        singles_events_obj = self.soup.find_all('li', class_='career-events disclaimer')
        if len(singles_events_obj) == 0:
            self.player_data.career_events = '0'
            return
        self.player_data.career_events = singles_events_obj[0].text.split(": ")[-1]

    def get_player_portrait_data(self, search_key: str | None = None) -> dict | None:
        search = search_key if search_key is not None else self.player_data.pdga_number
        try:
            player_portrait_data = None
            for img in self.soup.find_all('img'):
                if search in img.attrs.get('alt', ''):
                    player_portrait_data = img.attrs.copy()
            self.player_data.portrait_url = player_portrait_data['src']
        except (KeyError, TypeError):
            self.player_data.portrait_url = None
            return None
        return player_portrait_data

    def find_official_data(self):
        official_obj = self.soup.find_all('li', class_='official')
        if len(official_obj) >= 1:
            self.player_data.official_status = official_obj[0].text.split(": ")[-1].strip()
            return
        self.player_data.official_status = 'n/a'

    def get_player_upcoming_events_data(self):
        try:
            # find all upcoming events
            upcoming_events_obj = self.soup.find_all("li", class_="upcoming-events")

            if len(upcoming_events_obj) == 0:
                # if no upcoming events, player might have 0 or just 1 upcoming event, aka next-event
                upcoming_events_obj = self.soup.find_all("li", class_="next-event")
                if len(upcoming_events_obj) >=1:
                    event_obj = self._get_next_event(next_event_data=upcoming_events_obj[0])
                    self.player_data.upcoming_events.append(event_obj)
                    return
            if len(upcoming_events_obj) >= 1:
                events_data_list = []
                for events_data in upcoming_events_obj:
                    events = events_data.find_all('li')
                    if len(events) == 0:
                        # next-event
                        events = events_data.find_all('a')

                    events_data_list.extend(events)
                for event in events_data_list:
                    # try to find the events start date and name

                    date_start, evt_name = event.text.split(": ")
                    # find the events dates (from to)
                    evt_date_from_to = event.contents[1]['title'].split(" on ")[-1]
                    # find the events href
                    href = event.contents[1]['href']
                    event_obj = PdgaEvent(url_host=self.url, url_path=href, title=evt_name, date_start=date_start, date_from_to=evt_date_from_to)
                    self.player_data.upcoming_events.append(event_obj)
            else:

                if self.player_data.player_name is None:
                    event_obj = PdgaEvent(url_host=self.url, url_path=f'player/{self.player_data.pdga_number}', title='PDGA Player profile', date_start='No upcoming events found', date_from_to='')
                else:
                    event_obj = PdgaEvent(url_host=self.url, url_path=f'player/{self.player_data.pdga_number}', title=f'{self.player_data.player_name}', date_start='No upcoming events found', date_from_to='')
                self.player_data.upcoming_events.append(event_obj)
        except:
            self.player_data.upcoming_events.append(PdgaEvent(url_host=self.url, url_path=f'player/{self.player_data.pdga_number}', title=f'Player profile upcoming events', date_start='Failed to retrieve upcoming events\n', date_from_to=''))

    def _get_next_event(self, next_event_data):
        href = None
        date_start = None
        date_from_to = None
        title = None

        for content_data in next_event_data.contents:
            if content_data.text.isspace():
                continue
            if href is None:
                if content_data.has_attr('href'):
                    href = content_data['href']
            if title is None:
                if content_data.has_attr('title'):
                    title = content_data['title']
        if len(title) >=12:
            parts = title.split(",")
            if len(parts) >=2:
                for part in parts:
                    if part.replace(" ", "").isalpha():
                        continue
                    if part.replace(" ", "").replace("-", "").isalnum():
                        year = ""
                        if part.rfind("-") >= 0:
                            year = part.split("-")[-1]
                        date_parts = part.split(" to ")
                        if len(date_parts) >=2:
                            date_start = date_parts[0].split(" ")[-1]
                            if len(date_start) in [5,6]:
                                date_start += " " + year
                        date_from_to = part.replace("on","").lstrip(" ")
        event_obj = PdgaEvent(url_host=self.url, url_path=href, title=title, date_start=date_start, date_from_to=date_from_to)
        return event_obj
