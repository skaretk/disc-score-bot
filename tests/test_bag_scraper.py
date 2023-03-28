import os
import sys
from context import scrapers
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

def test_discgolfbagbuilder_bag_scraper():
    search = "https://www.discgolfbagbuilder.com/bags/oyv10ykqvre0jibt"
    scraper = scrapers.discgolfbagbuilder.DiscgolfBagBuilder(search)
    assert scraper.distance_drivers is None
    assert scraper.fairway_drivers is None
    assert scraper.midranges is None
    assert scraper.putt_approach is None

    scraper.scrape_discs()
    assert len(scraper.distance_drivers) == 9
    assert len(scraper.fairway_drivers) == 6
    assert len(scraper.midranges) == 3
    assert len(scraper.putt_approach) == 8
