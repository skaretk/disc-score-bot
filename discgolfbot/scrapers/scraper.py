import os
import time
import urllib.parse
#from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

# Base class
class Scraper():
    def __init__(self):
        self.name = ''
        self.url = ''
        self._scrape_url = ''
        self._scraper_time = ''
    
    @property
    def scrape_url(self):
        return self._scrape_url

    @scrape_url.setter
    def scrape_url(self, url):
        self._scrape_url = urllib.parse.quote(url, safe='?:/=&+')
    
    @property
    def scraper_time(self):
        return round(self._scraper_time, 2)

    @scraper_time.setter
    def scraper_time(self, time):
        self._scraper_time = time
    
    def get_chrome(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument("--headless")
        #opt.add_argument("--start-maximized")
        #opt.add_argument("--lang=nb-NO")
        opt.add_argument("--disable-extensions")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--disable-xss-auditor")
        #opt.add_argument("--disable-web-security")
        #opt.add_argument("--allow-running-insecure-content")
        opt.add_argument("--no-sandbox") # apparently as Docker deamon always runs as a root user, Chrome crushes.
        opt.add_argument("--disable-dev-shm-usage") # Explicitly disabling the usage of /dev/shm/ . The /dev/shm partition is too small in certain VM environments, causing Chrome to fail or crash.
        opt.add_argument("--disable-setuid-sandbox")
        opt.add_argument("--disable-webgl")
        opt.add_argument("--disable-popup-blocking)")
        opt.page_load_strategy = 'eager'
        
        chrome_prefs = {}
        opt.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}

        browser = webdriver.Chrome(options=opt) 
        browser.implicitly_wait(10)
        browser.set_page_load_timeout(30)
        return browser
    
    def get_page(self, sleep_time = 0):
        with self.get_chrome() as driver:
            driver.get(self.scrape_url)
            if sleep_time:
                time.sleep(sleep_time)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            return soup
    
    # Driver needs to be closed afterwards
    def get_driver(self, sleep_time = 0):
        driver = self.get_chrome()
        driver.get(self.scrape_url)
        if sleep_time:
            time.sleep(sleep_time)
        return driver
    
    # Driver needs to be closed afterwards
    def get_page_and_driver(self, sleep_time = 0):
        driver = self.get_chrome()
        driver.get(self.scrape_url)
        if sleep_time:
            time.sleep(sleep_time)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        return soup, driver
    
    # Driver needs to be closed afterwards
    def get_page_from_driver(self, driver):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        return soup
    
    def urllib_get_beatifulsoup(self, sleep_time = 0):
        sock = urlopen(self.scrape_url)
        if sleep_time:
            time.sleep(sleep_time)
        htmlSource = sock.read()
        return BeautifulSoup(htmlSource, "html.parser")
    
    def urllib_header_get_beatifulsoup(self, headers={}, sleep_time = 0):
        default_headers = {'User-Agent': 'Mozilla/5.0'}
        req_headers = dict(default_headers)
        req_headers.update(headers)
        req = Request(self.scrape_url, headers=req_headers)
        sock = urlopen(req)
        if sleep_time:
            time.sleep(sleep_time)
        htmlSource = sock.read()
        return BeautifulSoup(htmlSource)

    async def scrape(self):
        pass
