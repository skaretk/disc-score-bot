import sys
from pathlib import Path
from context import scrapers
from scrapers.discgolfbagbuilder import DiscgolfBagBuilder
sys.path.insert(0, str(Path().cwd()))

def test_discgolfbagbuilder_bag_scraper():
    search = "https://www.discgolfbagbuilder.com/bags/oyv10ykqvre0jibt"
    scraper = DiscgolfBagBuilder(search)
    assert scraper.distance_drivers is None
    assert scraper.fairway_drivers is None
    assert scraper.midranges is None
    assert scraper.putt_approach is None

    scraper.scrape_discs()
    assert len(scraper.distance_drivers) == 9
    assert len(scraper.fairway_drivers) == 6
    assert len(scraper.midranges) == 3
    assert len(scraper.putt_approach) == 8
