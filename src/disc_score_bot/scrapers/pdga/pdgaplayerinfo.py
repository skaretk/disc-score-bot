"""PdgaPlayerInfo dataclass for storing information about a PDGA player."""
from dataclasses import dataclass, field

@dataclass
class PdgaPlayerRating:
    """Dataclass for a PDGA player's rating"""
    current: str = ''
    change: str = ''

@dataclass
class PdgaMembership:
    """Dataclass for a PDGA player's membership status"""
    status: str = ''
    member_since: str = ''
    official_status: str = ''

@dataclass
class PdgaCareer:
    """Dataclass for a PDGA player's career"""
    events: str = ''
    wins: str = ''
    earnings: str = ''
    upcoming_events: list = field(default_factory=list)

@dataclass # pylint: disable=too-many-instance-attributes
class PdgaPlayerInfo:
    """Dataclass for a PdgaPlayer"""
    player_name: str = ''
    pdga_number: str = ''
    portrait_url: str = ''
    location: str = ''
    classification: str = ''
    membership: PdgaMembership = field(default_factory=PdgaMembership)
    rating: PdgaPlayerRating = field(default_factory=PdgaPlayerRating)
    events: PdgaCareer = field(default_factory=PdgaCareer)

    @property
    def dictionary(self):
        """Returns a dictionary of player information"""
        return {
            "Player Name": self.player_name,
            "PDGA Number": self.pdga_number,
            "Portrait URL": self.portrait_url,
            "Location": self.location,
            "Classification": self.classification,
            "Member Since": self.membership.member_since,
            "Membership Status": self.membership.status,
            "Official Status": self.membership.official_status,
            "Current Rating": self.rating.current,
            "Ratings Change": self.rating.change,
            "Career Events": self.events.events,
            "Career Wins": self.events.wins,
            "Career Earnings": self.events.earnings,
            "Upcoming Events": self.events.upcoming_events,
        }
