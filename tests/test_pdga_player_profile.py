import random
import pytest
from disc_score_bot.scrapers import pdga
from disc_score_bot.scrapers.pdga.pdgaevent import PdgaEvent
from disc_score_bot.pdga.pdgaplayerstat import PdgaPlayerStat

def check_player_profile_data(player_info) -> bool:
    """Check if the player profile data contains all required fields"""
    required = (
        player_info.pdga_number,
        player_info.player_name,
        player_info.rating.current,
        player_info.rating.change,
        player_info.location,
        player_info.classification,
        player_info.membership.member_since,
        player_info.membership.status,
        player_info.membership.official_status,
        player_info.events.events,
        player_info.events.upcoming_events,
        player_info.events.wins,
        player_info.events.earnings
        # portrait_url not included because it's not always present
    )
    return all(required)

@pytest.mark.parametrize("pdga_number_profile", [
    pytest.param("1",                                  id="steady_ed_expired_membership"),
    pytest.param(str(random.randrange(25000, 250000)), id="random"),
    pytest.param("75412",                              id="gannon_buhr_mpo"),
    pytest.param("48976",                              id="ohn_scoggings_fpo"),
])

def test_pdga_player_profile_scraper(pdga_number_profile):
    """Integration test: scrape the specified players"""
    scraper = pdga.PlayerProfileScraper(pdga_number=pdga_number_profile)
    scraper.scrape()
    assert check_player_profile_data(scraper.player_info) is True
    assert len(scraper.player_info.dictionary) != 0

@pytest.mark.parametrize("pdga_number_events", [
    pytest.param("75412", id="gannon_buhr_mpo"),
    pytest.param("48976", id="ohn_scoggings_fpo"),
])

def test_upcoming_pdga_events(pdga_number_events):
    """Integration test: scrape the specified players"""
    scraper = pdga.PlayerProfileScraper(pdga_number=pdga_number_events)
    scraper.scrape()

    events = scraper.player_info.events.upcoming_events
    assert isinstance(events, list)
    assert len(events) > 0, "Expected at least one upcoming event for this player"

    for event in events:
        assert isinstance(event, PdgaEvent)
        assert isinstance(event.name, str) and len(event.name) > 0, "Event name should be a non-empty string"
        assert isinstance(event.date_start, str) and len(event.date_start) > 0, "Event date_start should be a non-empty string"
        assert isinstance(event.event_url, str) and event.event_url.startswith("https://"), "Event URL should be a valid https URL"
        assert isinstance(event.location, str), "Event location should be a string"

    # Verify is_upcoming_event identifies at least one event within a generous 365-day window
    stat = PdgaPlayerStat.__new__(PdgaPlayerStat)
    soon = [e for e in events if stat.is_upcoming_event(e, days=365)]
    assert len(soon) > 0, "Expected at least one event within the next 365 days"


class TestPdgaEventDates:
    """Unit tests for PdgaEvent date_start / date_end parsing."""
    URL_HOST = "https://www.pdga.com/"
    def _make_event(self, date_start, dates):
        return PdgaEvent(url_host=self.URL_HOST, url_path="tour/event/1", name="Test Event", location="", date_start=date_start, dates=dates)

    def test_single_date_event_sets_date_end_equal_to_date_start(self):
        """When dates has no ' to ', date_end should equal date_start."""
        event = self._make_event(date_start="Sat, Apr 25, 2026", dates="25-Apr-2026")
        assert event.date_start == "25.04.2026"
        assert event.date_end == event.date_start

    def test_multi_date_event_parses_start_and_end(self):
        """When dates contains ' to ', start and end should be parsed independently."""
        event = self._make_event(date_start="Sat, Apr 25, 2026", dates="25-Apr to 26-Apr-2026")
        assert event.date_start == "25.04.2026"
        assert event.date_end == "26.04.2026"

    def test_multi_date_event_year_inherited_from_end(self):
        """Year in the end part must not bleed into date_start parsing."""
        event = self._make_event(date_start="Sat, Apr 25, 2026", dates="25-Apr to 26-Apr-2026")
        assert event.date_start == "25.04.2026", "date_start should be the 25th, not the 26th"
