import random
import pytest
from disc_score_bot.scrapers import pdga

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

@pytest.mark.parametrize("pdga_number", [
    pytest.param("1",                                  id="steady_ed_expired_membership"),
    pytest.param("182349",                             id="frode_kallevig"),
    pytest.param(str(random.randrange(25000, 250000)), id="random"),
    pytest.param("45971",                              id="calvin_heimburg_mpo"),
    pytest.param("73986",                              id="kristin_tattar_fpo"),
])

def test_pdga_player_profile_scraper(pdga_number):
    scraper = pdga.PlayerProfileScraper(pdga_number=pdga_number)
    scraper.scrape()
    assert check_player_profile_data(scraper.player_info) is True
    assert len(scraper.player_info.dictionary) != 0
