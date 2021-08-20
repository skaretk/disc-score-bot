import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

class Disc():
    def __init__(self):
        self.name = ''
        self.manufacturer = ''
        self.price = ''
        self.store = ''
        self.url = ''

class Scraper():
    def __init__(self, disc_search):
        self.url = ''
        self.search_url = ''
        self.disc_search = disc_search
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

    async def scrape(self):
        pass

class DiscInStock(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search)
        self.search_url = 'https://www.discinstock.no/?name='
    
    async def scrape(self):
        with self.get_chrome() as driver:
            url = urllib.parse.quote(f'{self.search_url}{self.disc_search}', safe='?:/=')
            driver.get(url)
            time.sleep(1)
            content = driver.page_source
            soup = BeautifulSoup(content, "html.parser")

            for a in soup.findAll("div", class_="col"):
                disc = Disc()
                disc.manufacturer = a.find("h6", class_="text-muted font-monospace h-100").getText()
                disc.name = a.find("span", class_="fs-5").getText()                
                disc.price = a.find("span", class_="flex-shrink-1 display-6 mt-1").getText()
                disc.store = a.find("span", class_="mx-auto text-muted").getText()
                link = a.find('a', href=True)
                disc.url = link['href']

                self.discs.append(disc)

class FrisbeeFeber(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search)
        self.url = 'frisbeefeber.no'
        self.search_url = 'https://www.frisbeefeber.no/search_result?keywords='
    
    async def scrape(self):
        with self.get_chrome() as driver:
            url = urllib.parse.quote(f'{self.search_url}{self.disc_search}', safe='?:/=&')
            driver.get(url)
            content = driver.page_source
            soup = BeautifulSoup(content, "html.parser")

            for product in soup.select('li[class*="product-box-id-"]'):
                # Is product in stock ?
                not_in_stock = product.find("div", class_="product not-in-stock-product")
                if (not_in_stock is not None):
                    continue
                disc = Disc()
                disc.name = product.find("a", class_="title col-md-12").getText()
                # Search engine gives false results, check if the disc name is correct
                if (self.disc_search.lower() not in disc.name.lower()):
                    continue
                div_manufacturer = product.find("div", class_="manufacturer-box")
                alt_manufacturer = div_manufacturer.find("img", alt=True)
                disc.manufacturer = alt_manufacturer['alt']
                disc.price = product.find("div", class_="price col-md-12").getText()
                disc.store = self.url
                link = product.find('a', href=True)
                disc.url = link['href']

                self.discs.append(disc) 

class Discconnection(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search)
        self.url = 'discconnection.dk'
        self.search_url = 'https://discconnection.dk/default.asp?page=productlist.asp&Search_Hovedgruppe=&Search_Undergruppe=&Search_Producent=&Search_Type=&Search_Model=&Search_Plastic=&PriceFrom=&PriceTo=&Search_FREE='
    
    async def scrape(self):
        with self.get_chrome() as driver:
            url = urllib.parse.quote(f'{self.search_url}{self.disc_search}', safe='?:/=&')
            driver.get(url)
            content = driver.page_source
            soup = BeautifulSoup(content, "html.parser")
            
            names = []
            manufacturers = []
            prices = []

            # Contains: "Innova Firebird  •  Plastic: Champion  •  Driver"
            for prodHeader in soup.findAll("td", class_="prodHeader"):
                b = prodHeader.find_all("b")
                prodHeader_list = b[0].getText().split()
                manufacturers.append(prodHeader_list[0])
                names.append(b[0].getText())

            # Contains: Pris inkl. moms: 120,00 DKK
            for prodPriceWeight in soup.findAll("td", class_="prodPriceWeight"):
                b = prodPriceWeight.find("b")
                if b is not None:
                    prices.append(b.getText())            

            for i in range(len(names)):
                disc = Disc()
                disc.name = names[i]
                disc.manufacturer = manufacturers[i]
                disc.price = prices[i]
                disc.store = self.url
                disc.url = url
                self.discs.append(disc)  