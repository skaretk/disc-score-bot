import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

import context
from context import scrapers

def test_armspeed_disc_scraper():
    search = "firebird"
    scraper = scrapers.armspeed.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_dgshop_disc_scraper():
    search = "firebird"
    scraper = scrapers.dgshop.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_discconnection_disc_scraper():
    search = "firebird"
    scraper = scrapers.discconnection.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_discexpress_disc_scraper():
    search = "firebird"
    scraper = scrapers.discexpress.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_discimport_disc_scraper():
    search = "firebird"
    scraper = scrapers.discimport.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_discinstock_disc_scraper():
    search = "firebird"
    scraper = scrapers.discinstock.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_discmania_disc_scraper():
    search = "tactic"
    scraper = scrapers.discmania.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_discrepublic_disc_scraper():
    search = "firebird"
    scraper = scrapers.discrepublic.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_discsport_disc_scraper():
    search = "firebird"
    scraper = scrapers.discsport.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_frisbeefeber_disc_scraper():
    search = "link"
    scraper = scrapers.frisbeefeber.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_gurudiscgolf_scraper():
    search = "firebird"
    scraper = scrapers.gurudiscgolf.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_krokholdgs_scraper():
    search = "firebird"
    scraper = scrapers.krokholdgs.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_latitude64_disc_scraper():
    search = "grace"
    scraper = scrapers.latitude64.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_rocketdiscs_disc_scraper():
    search = "firebird"
    scraper = scrapers.rocketdiscs.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_sunesport_disc_scraper():
    search = "firebird"
    scraper = scrapers.sunesport.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_xxl_disc_scraper():
    search = "harp"
    scraper = scrapers.xxl.DiscScraper(search)
    scraper.scrape()
    assert len(scraper.discs) != 0

def test_pdga_disc_scraper():
    scraper = scrapers.pdga.DiscScraper()
    scraper.scrape()
    assert len(scraper.discs) != 0
