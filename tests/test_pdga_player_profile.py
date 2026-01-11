import os
import random
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

def scrape_and_check(scraper):
    scraper.scrape()
    assert check_player_profile_data(scraper.player_data) is True
    assert len(scraper.player_data.dictionary) != 0


def test_pdga_player_profile_active_expired_membership_scraper():
    scrape_and_check(pdga.PlayerProfileScraper(pdga_number="1")) # Steady Ed

def test_pdga_player_profile_random_membership_scraper():
    scrape_and_check(pdga.PlayerProfileScraper(pdga_number=f"{random.randrange(25000,250000)}"))

def test_pdga_player_profile_active_current_membership_mpo_no_1_scraper():
    scrape_and_check(pdga.PlayerProfileScraper(pdga_number="45971")) # Calvin Heimburg

def test_pdga_player_profile_active_current_membership_fpo_no_1_scraper():
    scrape_and_check(pdga.PlayerProfileScraper(pdga_number="73986")) # Kristin Tattar
