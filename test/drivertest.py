import time
import re
import urllib.parse
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_browser():
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
    browser.implicitly_wait(1)
    browser.set_page_load_timeout(3)
    return browser

def find_disc(disc_name):
    start_time = time.time()
    url = 'https://rocketdiscs.com'
    browser = get_browser()
    with browser as driver:
        # driver.implicitly_wait(0)
        driver.get(url)
        element = driver.find_element_by_xpath('//*[@id="txtHeaderSearchText"]')
        element.send_keys(disc_name)
        driver.find_element_by_xpath('//*[@id="btnHeaderBasicSearch"]').click()

        disc = None
        found = True
        try:
          disc = driver.find_element_by_xpath('//*[@id="category-desc"]/div/h4')
        except:
          found = False
      
        if not found:
          print("Disc was not found")
      # return
    
        print("Find logic")
    # If found
    # driver.find_element_by_xpath('/html/body/form/section[2]/div/main/div[2]/div/div/div/h4/a').click()
    
        end_time = time.time()
        print(f'Spent {end_time - start_time} scraping')
        # time.sleep(10)

find_disc("roc3")
find_disc("bali")


