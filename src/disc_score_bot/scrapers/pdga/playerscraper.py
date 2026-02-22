from dateutil.parser import parse as parse_date
import time
import logging
from .pdga import Pdga
from .playerdata import PdgaEvent, PdgaPlayerData

logger = logging.getLogger(__name__)

class PlayerProfileScraper(Pdga):
    """Scraper for PDGA Player Profiles"""
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

        self.player_data.location = self._parse_location()
        self.player_data.membership_status = self._parse_membership_status()
        self.player_data.official_status = self._parse_official_status()
        self.player_data.current_rating = self._parse_current_rating()
        self.player_data.rating_change = self._parse_rating_change()

        # try to find player portrait data (url and player name)
        portrait_data = self._parse_portrait_data()
        self.player_data.portrait_url = portrait_data['src'] if portrait_data else None
        if portrait_data:
            self.player_data.player_name = portrait_data['alt'].split(self.player_data.pdga_number)[0].strip()
        else:
            self.player_data.player_name = self._parse_player_name()
            if not self.player_data.portrait_url and self.player_data.player_name:
                fallback = self._parse_portrait_data(search_key="'s picture")
                self.player_data.portrait_url = fallback['src'] if fallback else None

        self.player_data.upcoming_events = self._parse_upcoming_events()
        self.player_data.career_events = self._parse_career_events()

        self.scraper_time = time.time() - start_time
        logger.info('PDGA PlayerProfileScraper scraper: %s', self.scraper_time)

    def _parse_player_name(self) -> str:
        player_name_metadata = self.soup.find(name="meta", property="og:title")
        if player_name_metadata and 'content' in player_name_metadata.attrs:
            return player_name_metadata.attrs['content'].split("#")[0].rstrip()
        return ''

    def _parse_current_rating(self):
        """Parse the current rating of the player from the soup object. Returns 'n/a' if not found."""
        current_rating_data = self.soup.find('li', class_='current-rating')
        return current_rating_data.text.split(": ")[-1].strip() if current_rating_data else 'n/a'

    def _parse_rating_change(self) -> str:
        rating_difference = self.soup.find(name='a', property='rating-difference gain')
        return rating_difference.text if rating_difference else 'n/a'

    def _parse_career_events(self) -> str:
        career_events = self.soup.find_all('li', class_='career-events disclaimer')
        return career_events[0].text.split(": ")[-1].strip() if career_events else '0'

    def _parse_portrait_data(self, search_key: str | None = None) -> dict | None:
        search = search_key if search_key is not None else self.player_data.pdga_number
        portrait_data = None
        for img in self.soup.find_all('img'):
            if search in img.attrs.get('alt', ''):
                portrait_data = img.attrs.copy()
        if portrait_data and 'src' in portrait_data:
            return portrait_data
        return None

    def _parse_location(self) -> str:
        location = self.soup.find('li', class_='location')
        return location.a.text if location else 'n/a'

    def _parse_membership_status(self) -> str:
        """Parse the membership status of the player from the soup object. Returns 'n/a' if not found."""
        membership_status = self.soup.find('li', class_='membership-status')
        return membership_status.text.split(": ")[-1].strip() if membership_status else 'n/a'

    def _parse_official_status(self) -> str:
        """Parse the official status of the player from the soup object. Returns 'n/a' if not found."""
        official = self.soup.find('li', class_='official')
        return official.text.split(": ")[-1].strip() if official else 'n/a'

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
        if title and len(title) >=12:
            date_start, date_from_to = self._parse_date_from_title(title)

        event = PdgaEvent(url_host=self.url, url_path=href, title=title, date_start=date_start, date_from_to=date_from_to)
        return event

    def _collect_next_event(self) -> list[PdgaEvent]:
        next_event = self.soup.find_all("li", class_="next-event")
        if next_event:
            return [self._get_next_event(next_event_data=next_event[0])]
        return [self._no_upcoming_events_obj()]

    def _collect_multiple_events(self, upcoming_events) -> list[PdgaEvent]:
        if not upcoming_events:
            return [self._no_upcoming_events_obj()]
        events_list = []
        for events_data in upcoming_events:
            events = events_data.find_all('li')
            if not events:
                events = events_data.find_all('a')
            events_list.extend(events)
        result = []
        for event in events_list:
            date_start, evt_name = event.text.split(": ")
            evt_date_from_to = event.contents[1]['title'].split(" on ")[-1]
            href = event.contents[1]['href']
            result.append(PdgaEvent(url_host=self.url, url_path=href, title=evt_name, date_start=date_start, date_from_to=evt_date_from_to))
        return result

    def _parse_upcoming_events(self) -> list[PdgaEvent]:
        try:
            upcoming_events = self.soup.find_all("li", class_="upcoming-events")
            if not upcoming_events:
                return self._collect_next_event()
            return self._collect_multiple_events(upcoming_events)
        except Exception as e:
            logger.warning("Failed to parse upcoming events: %s", e)
            return [self._failed_upcoming_events_obj()]

    def _no_upcoming_events_obj(self) -> PdgaEvent:
        title = self.player_data.player_name or 'PDGA Player profile'
        return PdgaEvent(
            url_host=self.url,
            url_path=f'player/{self.player_data.pdga_number}',
            title=title,
            date_start='No upcoming events found',
            date_from_to=''
        )

    def _failed_upcoming_events_obj(self) -> PdgaEvent:
        return PdgaEvent(
            url_host=self.url,
            url_path=f'player/{self.player_data.pdga_number}',
            title='Player profile upcoming events',
            date_start='Failed to retrieve upcoming events\n',
            date_from_to=''
        )

    def _parse_date_from_title(self, title: str) -> tuple[str | None, str | None]:
        """Extract date_start and date_from_to from event title string."""
        parts = title.split(",")
        for part in parts:
            stripped = part.replace(" ", "")
            if stripped.isalpha():
                continue
            try:
                date_start = parse_date(part.strip(), fuzzy=True).strftime("%a, %b %d, %Y")
                return date_start, part.strip()
            except ValueError:
                continue
        return None, None

