import random
import pytest
from disc_score_bot.scrapers import pdga

def check_player_profile_data(player_data) -> bool:
    required = (
        player_data.pdga_number,
        player_data.player_name,
        player_data.current_rating,
        player_data.rating_change,
        player_data.location,
        player_data.membership_status,
        player_data.official_status,
        player_data.career_events,
        player_data.upcoming_events,
        # portrait_url is not included because it's not always present
    )
    return all(required)

@pytest.mark.parametrize("pdga_number", [
    pytest.param("1",                                  id="steady_ed_expired_membership"),
    pytest.param("182349",                             id="frode_kallevig"),
    pytest.param(str(random.randrange(25000, 250000)), id="random"),
    pytest.param("45971",                              id="calvin_heimburg_mpo_no1"),
    pytest.param("73986",                              id="kristin_tattar_fpo_no1"),
])

def test_pdga_player_profile_scraper(pdga_number):
    scraper = pdga.PlayerProfileScraper(pdga_number=pdga_number)
    scraper.scrape()
    assert check_player_profile_data(scraper.player_data) is True
    assert len(scraper.player_data.dictionary) != 0
