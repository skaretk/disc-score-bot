"""PdgaEvent dataclass for storing information about a PDGA event."""
from dataclasses import dataclass, field, InitVar
from datetime import datetime

import urllib

@dataclass
class PdgaEvent:
    """Dataclass for a PdgaEvent"""
    url_host: InitVar[str]
    url_path: InitVar[str]
    name: str
    date_start: str | None
    date_from_to: str
    location: str = ''
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
        return f'{self.date_start}: [{self.name}]({self.event_url})'
