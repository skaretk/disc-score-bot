import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

import context
from context import scrapers

def test_discgolfbagbuilder_bag_scraper():
    search = "https://www.discgolfbagbuilder.com/bags/oyv10ykqvre0jibt"
    scraper = scrapers.discgolfbagbuilder.DiscgolfBagBuilder(search)
    scraper.scrape_discs()
    assert scraper.distance_drivers is not None
    assert scraper.distance_drivers is not None
    assert scraper.fairway_drivers is not None
    assert scraper.midranges is not None
    assert scraper.putt_approach is not None
