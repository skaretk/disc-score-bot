import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from bs4 import BeautifulSoup

class Scraper():
    def __init__(self, search):
        self.url = ''
        self.search_url = ''
        self.search = search
        self.search_time = ''
        self.discs = []
    
    def get_chrome(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument("--headless")
        opt.add_argument("--disable-extensions")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--disable-xss-auditor")
        #opt.add_argument("--disable-web-security")
        #opt.add_argument("--allow-running-insecure-content")
        #opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-setuid-sandbox")
        opt.add_argument("--disable-webgl")
        opt.add_argument("--disable-popup-blocking")
        opt.page_load_strategy = 'eager'
        browser = webdriver.Chrome(options=opt)
        browser.implicitly_wait(10)
        browser.set_page_load_timeout(30)
        return browser
    
    def get_page(self, sleep_time = 0):
        with self.get_chrome() as driver:
            url = urllib.parse.quote(self.search_url, safe='?:/=&+')
            driver.get(url)
            if sleep_time:
                time.sleep(sleep_time)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            return soup
    
    # Driver needs to be closed afterwards
    def get_driver(self, sleep_time = 0):
        driver = self.get_chrome()
        url = urllib.parse.quote(self.search_url, safe='?:/=&+')
        driver.get(url)
        if sleep_time:
            time.sleep(sleep_time)
        return driver
    
    # Driver needs to be closed afterwards
    def get_page_and_driver(self, sleep_time = 0):
        driver = self.get_chrome()
        url = urllib.parse.quote(self.search_url, safe='?:/=&+')
        driver.get(url)
        if sleep_time:
            time.sleep(sleep_time)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        return soup, driver

    def get_search_time(self):
        return round(self.search_time, 2)

    async def scrape(self):
        pass
