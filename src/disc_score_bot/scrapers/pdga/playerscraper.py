"""Scraper for PDGA Player Profiles"""
import time
import logging
from dateutil.parser import parse as parse_date
from .pdga import Pdga
from .pdgaplayerinfo import PdgaPlayerInfo
from .pdgaevent import PdgaEvent

logger = logging.getLogger(__name__)

class PlayerProfileScraper(Pdga):
    """Scraper for PDGA Player Profiles"""
    def __init__(self, pdga_number):
        super().__init__()
        self.name = "PDGA Player Profile"
        self.scrape_url = f'{self.url}player/{pdga_number}'
        self.player_info = PdgaPlayerInfo(pdga_number=pdga_number)
        self._player_info = None

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
        self._player_info = self.soup.find('ul', class_='player-info')

        self.player_info.location = self._parse_location()
        self.player_info.classification = self._parse_classification()
        self.player_info.membership.member_since = self._parse_member_since()
        self.player_info.membership.status = self._parse_membership_status()
        self.player_info.membership.official_status = self._parse_official_status()
        self.player_info.rating.current = self._parse_current_rating()
        self.player_info.rating.change = self._parse_rating_change()

        # try to find player portrait data (url and player name)
        self._parse_portrait_and_name()

        self.player_info.events.events = self._parse_career_events()
        self.player_info.events.wins = self._parse_career_wins()
        self.player_info.events.earnings = self._parse_career_earnings()
        self.player_info.events.upcoming_events = self._parse_upcoming_events()

        self.scraper_time = time.time() - start_time
        logger.info('PDGA PlayerProfileScraper scraper: %s', self.scraper_time)

    def _parse_location(self) -> str:
        """Parse the location of the player. Returns 'n/a' if not found."""
        location = self._player_info.find('li', class_='location')
        return location.a.text if location else 'n/a'

    def _parse_classification(self) -> str:
        """Parse the classification of the player. Returns 'n/a' if not found."""
        classification = self._player_info.find('li', class_='classification')
        return classification.text.split(": ")[-1].strip() if classification else 'n/a'

    def _parse_member_since(self) -> str:
        """Parse the member since date of the player. Returns 'n/a' if not found."""
        member_since = self._player_info.find('li', class_='join-date')
        return member_since.text.split(": ")[-1].strip() if member_since else 'n/a'

    def _parse_membership_status(self) -> str:
        """Parse the membership status of the player. Returns 'n/a' if not found."""
        membership_status = self._player_info.find('li', class_='membership-status')
        return membership_status.text.split(": ")[-1].strip() if membership_status else 'n/a'

    def _parse_official_status(self) -> str:
        """Parse the official status of the player. Returns 'n/a' if not found."""
        official = self._player_info.find('li', class_='official')
        return official.text.split(": ")[-1].strip() if official else 'n/a'

    def _parse_current_rating(self) -> str:
        """Parse the current rating of the player. Returns 'n/a' if not found."""
        current_rating_data = self._player_info.find('li', class_='current-rating')
        return current_rating_data.text.split(": ")[-1].strip() if current_rating_data else 'n/a'

    def _parse_player_name(self) -> str:
        """Parse the player's name. Returns an empty string if not found."""
        pane = self.soup.find('div', class_='pane-content')
        h1 = pane.find('h1') if pane else None
        if h1:
            return h1.text.split("#")[0].rstrip()
        meta = self.soup.find(name="meta", property="og:title")
        if meta and 'content' in meta.attrs:
            return meta.attrs['content'].split("#")[0].rstrip()
        return ''

    def _parse_rating_change(self) -> str:
        """Parse the rating change of the player. Returns 'n/a' if not found."""
        rating_difference = self.soup.find(name='a', property='rating-difference gain')
        return rating_difference.text if rating_difference else 'n/a'

    def _parse_career_events(self) -> str:
        """Parse the career events of the player. Returns '0' if not found."""
        career_events = self._player_info.find('li', class_='career-events disclaimer')
        return career_events.text.split(": ")[-1].strip() if career_events else '0'

    def _parse_career_wins(self) -> str:
        """Parse the career wins of the player. Returns '0' if not found."""
        career_wins = self._player_info.find('li', class_='career-wins disclaimer')
        return career_wins.text.split(": ")[-1].strip() if career_wins else '0'

    def _parse_career_earnings(self) -> str:
        """Parse the career earnings of the player. Returns 'n/a' if not found."""
        career_earnings = self._player_info.find('li', class_='career-earnings')
        return career_earnings.text.split(": ")[-1].strip() if career_earnings else 'n/a'

    def _parse_portrait_and_name(self) -> None:
        """Parse portrait URL and player name, with fallbacks for both."""
        portrait_data = self._parse_portrait_data()
        self.player_info.portrait_url = portrait_data['src'] if portrait_data else None
        if portrait_data:
            self.player_info.player_name = portrait_data['alt'].split(self.player_info.pdga_number)[0].strip()
        else:
            self.player_info.player_name = self._parse_player_name()
            if self.player_info.player_name:
                fallback = self._parse_portrait_data(search_key="'s picture")
                self.player_info.portrait_url = fallback['src'] if fallback else None

    def _parse_portrait_data(self, search_key: str | None = None) -> dict | None:
        """Parse the portrait data of the player. Returns a dictionary with 'src' and 'alt' if found, otherwise None."""
        search = search_key if search_key is not None else self.player_info.pdga_number
        portrait_data = None
        for img in self.soup.find_all('img'):
            if search in img.attrs.get('alt', ''):
                portrait_data = img.attrs.copy()
        if portrait_data and 'src' in portrait_data:
            return portrait_data
        return None

    def _get_next_event(self, next_event_data) -> PdgaEvent:
        link = next_event_data.find('a', href=True, title=True)
        href = link['href'] if link else None
        title = link['title'] if link else None
        date_start, date_from_to = self._parse_date_from_title(title) if title and len(title) >= 12 else (None, None)
        name = link.get_text(strip=True) if link else None
        location = title.split(' in ', 1)[1].split(',')[0].strip() if title and ' in ' in title else ''
        return PdgaEvent(url_host=self.url, url_path=href, name=name, location=location, date_start=date_start, date_from_to=date_from_to)

    def _collect_next_event(self) -> list[PdgaEvent]:
        next_event = self._player_info.find("li", class_="next-event")
        if next_event:
            return [self._get_next_event(next_event)]
        return [self._no_upcoming_events_obj()]

    def _collect_multiple_events(self, upcoming_events) -> list[PdgaEvent]:
        result = []
        for events_data in upcoming_events:
            events = events_data.find_all('li') or events_data.find_all('a')
            for event in events:
                date_start, evt_name = event.text.split(": ", 1)
                link = event.contents[1]
                event_title = link['title']
                event_location = event_title.split(' in ', 1)[1].split(',')[0].strip() if ' in ' in event_title else ''
                result.append(PdgaEvent(
                    url_host=self.url,
                    url_path=link['href'],
                    name=evt_name,
                    location=event_location,
                    date_start=date_start,
                    date_from_to=event_title.split(' on ')[-1]
                ))
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
        title = self.player_info.player_name or 'PDGA Player profile'
        return PdgaEvent(
            url_host=self.url,
            url_path=f'player/{self.player_info.pdga_number}',
            name=title,
            date_start='No upcoming events found',
            date_from_to=''
        )

    def _failed_upcoming_events_obj(self) -> PdgaEvent:
        return PdgaEvent(
            url_host=self.url,
            url_path=f'player/{self.player_info.pdga_number}',
            name='Player profile upcoming events',
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
