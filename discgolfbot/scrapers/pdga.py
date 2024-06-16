import time
from disc.pdgaapproveddisc import PdgaApprovedDisc
from .scraper import Scraper
import re
import urllib.parse

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

        manufacturers = soup.findAll("td", class_="views-field views-field-field-equipment-manuf-ref")
        disc_models = soup.findAll("td", class_="views-field views-field-title")
        approved_dates = soup.findAll("td", class_="views-field views-field-field-equipment-approve-date")

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
        print(f'PDGA scraper: {self.scraper_time}')

class PdgaPlayerData():
    def __init__(self, pdga_number):
        self.pdga_number = pdga_number
        self.current_rating = 0
        self.rating_change = 0
        self.location = ''
        self.membership_status = ''
        self.offical_status = ''
        self.career_events = 0
        self.upcoming_events = []
        self.portrait_url = ''
        self.player_name = ''

    @property
    def dictionary(self):
        """Returns a dictionary"""
        return {
            "Current Rating": self.current_rating,
            "Career Events": self.career_events,
            "Location": self.location,
            "Membership Status": self.membership_status,
            "Official Status": self.offical_status,
            "PDGA Number": self.pdga_number,
            "Ratings Change": self.rating_change,
            "Upcoming Events": self.upcoming_events,
        }

class PdgaEvent():
    def __init__(self, url_host:str, url_path:str, title:str, date_start:str, date_from_to:str) -> None:
        # day, month(str3) month-day(int1-2), year(int4)
        self._rexpression = re.compile(pattern='\w{3},\s\w{3}\s(?:(\d)),\s\d{4}', flags=re.IGNORECASE)
        self.event_url = urllib.parse.urljoin(base=url_host, url=url_path)
        self.title = title
        self.date_start = date_start
        self.date_from_to = date_from_to
        self.__on_init__()

    def __on_init__(self):
        day_in_month = self._rexpression.findall(string=self.date_start)
        if len(day_in_month) == 1:
            if len(day_in_month[0]) == 1:
                replace_day_in_month = "0" + day_in_month[0]
                self.date_start = self.date_start.replace(day_in_month[0], replace_day_in_month, 1)

    def __repr__(self) -> str:
        return f'{self.date_start}: [{self.title}]({self.event_url})'

class PlayerProfileScraper(Pdga):
    def __init__(self, pdga_number):
        super().__init__()
        self.name = "PDGA Player Profile"
        self.scrape_url = f'{self.url}player/{pdga_number}'
        self.pdga_number = pdga_number
        self.player_data = PdgaPlayerData(pdga_number)

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
        loc_obj = self.soup.find_all('li', 'location')
        self.player_data.location = loc_obj[0].a.text
        # find the membership status of the player
        membership_obj = self.soup.find_all('li', 'membership-status')
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
            self.find_player_name(tag="meta", tag_property="og:title")
            if self.player_data.portrait_url is None and self.player_data.player_name:
                self.get_player_portrait_data(search_key="'s picture")

        # parse players upcoming event and assemble a string worthy of discord-embeds :)
        self.get_player_upcoming_events_data()

        # find the past events data
        self.get_singles_event_history()

        # print the chore
        self.scraper_time = time.time() - start_time
        print(f'PDGA scraper: {self.scraper_time}')

    def find_player_name(self, tag="meta", tag_property="og:title"):
        player_name = '-'
        player_name_metadata = self.soup.find(name=tag, property=tag_property)
        if 'content' in player_name_metadata.attrs:
            player_name = player_name_metadata.attrs['content'].split("#")[0].rstrip()
        self.player_data.player_name = player_name

    def find_current_rating(self):
        current_rating_data = self.soup.find('li', 'current-rating')
        if current_rating_data is None:
            self.player_data.current_rating = 'n/a'
            return
        self.player_data.current_rating = current_rating_data.text.split(": ")[-1].strip()


    def find_rating_difference_gain(self):
        rating_diff_data = self.soup.find_all(name='a', property='rating-difference gain')
        if len(rating_diff_data) == 0:
            self.player_data.rating_change = 'n/a'
            return
        self.player_data.rating_change = rating_diff_data[0].find_all(name='a', property='rating-difference gain')[0].text

    def get_singles_event_history(self):
        singles_events_obj = self.soup.find_all('li', 'career-events disclaimer')
        if len(singles_events_obj) == 0:
            self.player_data.career_events = '0'
            return
        self.player_data.career_events = singles_events_obj[0].text.split(": ")[-1]

    def get_player_portrait_data(self, search_key=None):
        try:
            if search_key is not None:
                reg_pat = search_key
            else:
                reg_pat = "\w+\s" +f"{self.player_data.pdga_number}"
            player_portrait_data = None
            regex_compile = re.compile(pattern=reg_pat, flags=re.IGNORECASE)
            port_data = self.soup.find_all('img')
            for pd in port_data:

                if regex_compile.search(string=pd.attrs['alt']):
                    player_portrait_data = pd.attrs.copy()
            self.player_data.portrait_url = player_portrait_data['src']
        except:
            self.player_data.portrait_url = None
            return None
        return player_portrait_data

    def find_official_data(self):
        official_obj = self.soup.find_all('li', 'official')
        if len(official_obj) >= 1:
            self.player_data.offical_status = official_obj[0].text.split(": ")[-1].strip()
            return
        self.player_data.offical_status = 'n/a'

    # commit to move over to work lap..
    def get_player_upcoming_events_data(self):
        try:
            # find all upcoming events
            upcoming_events_obj = self.soup.find_all("li", "upcoming-events")

            if len(upcoming_events_obj) == 0:
                # if no upcoming events, player might have 0 or just 1 upcoming event, aka next-event
                upcoming_events_obj = self.soup.find_all("li", "next-event")
                if len(upcoming_events_obj) >=1:
                    event_obj = self.__get_next_event__(next_event_data=upcoming_events_obj[0])
                    self.player_data.upcoming_events.append(event_obj)
                    return
                # player_upcoming_events = "```yaml\n"
            if len(upcoming_events_obj) >= 1:
                events_data_list = []
                for events_data in upcoming_events_obj: #[0].find_all('a'):
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
                    event_obj = PdgaEvent(url_host=self.url, url_path=f'player/{self.pdga_number}', title='PDGA Player profile', date_start='No upcoming events found', date_from_to='')
                else:
                    event_obj = PdgaEvent(url_host=self.url, url_path=f'player/{self.pdga_number}', title=f'{self.player_data.player_name}', date_start='No upcoming events found', date_from_to='')
                self.player_data.upcoming_events.append(event_obj)
        except:
            self.player_data.upcoming_events.append(PdgaEvent(url_host=self.url, url_path=f'player/{self.pdga_number}', title=f'Player profile upcoming events', date_start='Failed to retrieve upcoming events\n', date_from_to=''))

    def __get_next_event__(self, next_event_data):
        href = None; date_start = None; date_from_to = None; title = None
        for content_data in next_event_data.contents:
            if str.isspace(content_data.text):
                continue
            if href is None:
                if content_data.has_key('href'):
                    href = content_data['href']
            if title is None:
                if content_data.has_key('title'):
                    title = content_data['title']
        if len(title) >=12:
            parts = title.split(",")
            if len(parts) >=2:
                for part in parts:
                    if str.isalpha(part.replace(" ","")):
                        continue
                    if str.isalnum(part.replace(" ","").replace("-","")):
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
        # if date_from_to is None:
