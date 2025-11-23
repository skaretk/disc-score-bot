import pytest
from disc_score_bot.scrapers import aceshop
from disc_score_bot.scrapers import armspeed
from disc_score_bot.scrapers import dgshop
from disc_score_bot.scrapers import discconnection
from disc_score_bot.scrapers import discexpress
from disc_score_bot.scrapers import discimport
from disc_score_bot.scrapers import discinstock
from disc_score_bot.scrapers import discmania
from disc_score_bot.scrapers import discrepublic
from disc_score_bot.scrapers import discsport
from disc_score_bot.scrapers import frisbeefeber
from disc_score_bot.scrapers import fyndisc
from disc_score_bot.scrapers import kastmeg
from disc_score_bot.scrapers import krokholdgs
from disc_score_bot.scrapers import latitude64
from disc_score_bot.scrapers import rocketdiscs
from disc_score_bot.scrapers import starframe
from disc_score_bot.scrapers import sunesport
from disc_score_bot.scrapers import wearediscgolf
from disc_score_bot.scrapers import xxl
from disc_score_bot.scrapers import pdga
from disc_score_bot.scrapers import rocketdiscs

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
        assert check_disc(disc) is True

def test_aceshop_disc_scraper():
    search = "firebird"
    scrape_and_check(aceshop.DiscScraper(search))

@pytest.mark.skip(reason="Site not available")
def test_armspeed_disc_scraper():
    search = "firebird"
    scrape_and_check(armspeed.DiscScraper(search))

def test_dgshop_disc_scraper():
    search = "firebird"
    scrape_and_check(dgshop.DiscScraper(search))

def test_discconnection_disc_scraper():
    search = "firebird"
    scrape_and_check(discconnection.DiscScraper(search))

def test_discexpress_disc_scraper():
    search = "firebird"
    scrape_and_check(discexpress.DiscScraper(search))

@pytest.mark.xfail
def test_discimport_disc_scraper():
    search = "firebird"
    scrape_and_check(discimport.DiscScraper(search))

@pytest.mark.xfail(reason="Scraper not updated")
def test_discinstock_disc_scraper():
    search = "firebird"
    scrape_and_check(discinstock.DiscScraper(search))

def test_discinstock_disc_scraper_api():
    search = "firebird"
    scrape_and_check(discinstock.DiscScraperApi(search))

def test_discmania_disc_scraper():
    search = "tactic"
    scrape_and_check(discmania.DiscScraper(search))

def test_discrepublic_disc_scraper():
    search = "firebird"
    scrape_and_check(discrepublic.DiscScraper(search))

@pytest.mark.xfail(reason="Scraper not updated")
def test_discsport_disc_scraper():
    search = "firebird"
    scrape_and_check(discsport.DiscScraper(search))

@pytest.mark.xfail
def test_frisbeefeber_disc_scraper():
    search = "link"
    scrape_and_check(frisbeefeber.DiscScraper(search))

@pytest.mark.xfail
def test_fyndisc_disc_scraper():
    search = "firebird"
    scrape_and_check(fyndisc.DiscScraper(search))

def test_kastmeg_scraper():
    search = "firebird"
    scrape_and_check(kastmeg.DiscScraper(search))

@pytest.mark.xfail(reason="Scraper needs to be updated")
def test_krokholdgs_scraper():
    search = "firebird"
    scrape_and_check(krokholdgs.DiscScraper(search))

@pytest.mark.xfail(reason="Scraper not updated")
def test_latitude64_disc_scraper():
    search = "grace"
    scrape_and_check(latitude64.DiscScraper(search))

@pytest.mark.xfail(reason="Scraper not updated")
def test_rocketdiscs_disc_scraper():
    search = "firebird"
    scrape_and_check(rocketdiscs.DiscScraper(search))

def test_starframe_disc_scraper():
    search = "firebird"
    scrape_and_check(starframe.DiscScraper(search))

@pytest.mark.xfail(reason="Scraper not updated")
def test_sunesport_disc_scraper():
    search = "firebird"
    scrape_and_check(sunesport.DiscScraper(search))

@pytest.mark.xfail(reason="Scraper not updated")
def test_wearediscgolf_scraper():
    search = "firebird"
    scrape_and_check(wearediscgolf.DiscScraper(search))

@pytest.mark.xfail(reason="Scraper not updated")
def test_xxl_disc_scraper():
    search = "harp"
    scrape_and_check(xxl.DiscScraper(search))

def test_pdga_disc_scraper():
    scraper = pdga.DiscScraper()
    scraper.scrape()
    assert len(scraper.discs) != 0
