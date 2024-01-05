import sys
from pathlib import Path
from context import scrapers
sys.path.insert(0, str(Path().cwd()))

def check_disc(disc):
    if not disc.name:
        return False
    if not disc.price:
        return False
    if not disc.price:
        return False
    if not disc.store:
        return False
    if not disc.url:
        return False
    if not disc.img:
        return False
    return True

def scrape_and_check(scraper):
    scraper.scrape()
    assert len(scraper.discs) != 0
    for disc in scraper.discs:
        assert check_disc(disc) == True

def test_aceshop_disc_scraper():
    search = "firebird"
    scrape_and_check(scrapers.aceshop.DiscScraper(search))

def test_armspeed_disc_scraper():
    search = "firebird"
    scrape_and_check(scrapers.armspeed.DiscScraper(search))

def test_dgshop_disc_scraper():
    search = "firebird"
    scrape_and_check(scrapers.dgshop.DiscScraper(search))

def test_discconnection_disc_scraper():
    search = "firebird"
    scrape_and_check(scrapers.discconnection.DiscScraper(search))

def test_discexpress_disc_scraper():
    search = "firebird"
    scrape_and_check(scrapers.discexpress.DiscScraper(search))

def test_discimport_disc_scraper():
    search = "firebird"
    scrape_and_check(scrapers.discimport.DiscScraper(search))

def test_discinstock_disc_scraper():
    search = "firebird"
    scrape_and_check(scrapers.discinstock.DiscScraper(search))

def test_discinstock_disc_scraper_api():
    search = "firebird"
    scrape_and_check(scrapers.discinstock.DiscScraperApi(search))

def test_discmania_disc_scraper():
    search = "tactic"
    scrape_and_check(scrapers.discmania.DiscScraper(search))

def test_discrepublic_disc_scraper():
    search = "firebird"
    scrape_and_check(scrapers.discrepublic.DiscScraper(search))

def test_discsport_disc_scraper():
    search = "firebird"
    scrape_and_check(scrapers.discsport.DiscScraper(search))

#def test_frisbeefeber_disc_scraper():
#    search = "link"
#    scrape_and_check(scrapers.frisbeefeber.DiscScraper(search))

#def test_fyndisc_disc_scraper():
#    search = "firebird"
#    scrape_and_check(scrapers.fyndisc.DiscScraper(search))

def test_kastmeg_scraper():
    search = "firebird"
    scrape_and_check(scrapers.kastmeg.DiscScraper(search))

def test_krokholdgs_scraper():
    search = "firebird"
    scrape_and_check(scrapers.krokholdgs.DiscScraper(search))

def test_latitude64_disc_scraper():
    search = "grace"
    scrape_and_check(scrapers.latitude64.DiscScraper(search))

def test_rocketdiscs_disc_scraper():
    search = "firebird"
    scrape_and_check(scrapers.rocketdiscs.DiscScraper(search))

def test_starframe_disc_scraper():
    search = "firebird"
    scrape_and_check(scrapers.starframe.DiscScraper(search))

#def test_sunesport_disc_scraper():
#    search = "firebird"
#    scrape_and_check(scrapers.sunesport.DiscScraper(search))

def test_wearediscgolf_scraper():
    search = "firebird"
    scrape_and_check(scrapers.wearediscgolf.DiscScraper(search))

#def test_xxl_disc_scraper():
#    search = "harp"
#    scrape_and_check(scrapers.xxl.DiscScraper(search))

def test_pdga_disc_scraper():
    scraper = scrapers.pdga.DiscScraper()
    scraper.scrape()
    assert len(scraper.discs) != 0
