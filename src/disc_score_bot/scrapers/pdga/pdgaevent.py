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
    dates: str
    date_start: str | None
    date_end: str | None = field(init=False, default=None)
    location: str = ''
    event_url: str = field(init=False)


    def __post_init__(self, url_host: str, url_path: str):
        self.event_url = urllib.parse.urljoin(base=url_host, url=url_path)
        if self.date_start is None:
            return
        try:
            parsed = datetime.strptime(self.date_start, "%a, %b %d, %Y")
            self.date_start = parsed.strftime("%d.%m.%Y")
        except ValueError:
            pass  # date_start is in an unrecognised format, leave as-is
        if self.dates and ' to ' in self.dates:
            end_str = self.dates.split(' to ', 1)[1].strip()
            for fmt in ("%d-%b-%Y", "%b %d, %Y", "%d %b %Y"):
                try:
                    self.date_end = datetime.strptime(end_str, fmt).strftime("%d.%m.%Y")
                    break
                except ValueError:
                    continue

    def __repr__(self) -> str:
        return f'{self.date_start}: [{self.name}]({self.event_url})'
