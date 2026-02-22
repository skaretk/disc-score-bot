from dataclasses import dataclass, field, InitVar
from datetime import datetime
import urllib.parse

@dataclass
class PdgaPlayerData:
    """Dataclass for a PdgaPlayer"""
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

@dataclass
class PdgaEvent:
    url_host: InitVar[str]
    url_path: InitVar[str]
    title: str
    date_start: str | None
    date_from_to: str
    event_url: str = field(init=False)

    def __post_init__(self, url_host: str, url_path: str):
        self.event_url = urllib.parse.urljoin(base=url_host, url=url_path)
        if self.date_start is None:
            return
        try:
            parsed = datetime.strptime(self.date_start, "%a, %b %d, %Y")
            self.date_start = parsed.strftime("%a, %b %d, %Y")
        except ValueError:
            pass  # date_start is in an unrecognised format, leave as-is

    def __repr__(self) -> str:
        return f'{self.date_start}: [{self.title}]({self.event_url})'