import os
import sys
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))
from context import scrapers


def check_player_profile_data(player_data):
    if not player_data.pdga_number:
        return False
    if not player_data.player_name:
        return False
    if not player_data.current_rating:
        return False
    if not player_data.rating_change:
        return False
    if not player_data.location:
        return False
    if not player_data.membership_status:
        return False
    if not player_data.offical_status:
        return False
    if not player_data.career_events:
        return False
    if not player_data.upcoming_events:
        return False
    # portrait_url is not included because it's not always present
    return True

def scrape_and_check(scraper):
    scraper.scrape()
    assert check_player_profile_data(scraper.player_data) is True
    assert len(scraper.player_data.dictionary) != 0


def test_pdga_player_profile_active_expired_membership_scraper():
    scrape_and_check(scrapers.pdga.PlayerProfileScraper(pdga_number="1")) # Steady Ed

def test_pdga_player_profile_random_membership_scraper():
    scrape_and_check(scrapers.pdga.PlayerProfileScraper(pdga_number=f"{random.randrange(25000,250000)}"))

def test_pdga_player_profile_active_current_membership_mpo_no_1_scraper():
    scrape_and_check(scrapers.pdga.PlayerProfileScraper(pdga_number="45971")) # Calvin Heimburg

def test_pdga_player_profile_active_current_membership_fpo_no_1_scraper():
    scrape_and_check(scrapers.pdga.PlayerProfileScraper(pdga_number="73986")) # Kristin Tattar
