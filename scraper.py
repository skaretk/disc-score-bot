import os
import time
import re
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, SoupStrainer
from lxml import etree

class Disc():
    def __init__(self):
        self.name = ''
        self.manufacturer = ''
        self.price = ''
        self.store = ''
        self.url = ''
        self.img_url = ''
        self.speed = ''
        self.glide = ''
        self.turn = ''
        self.fade = ''
        
    def __str__(self):
        return f'name: {self.name}\n'\
               f'manufacturer: {self.manufacturer}\n'\
               f'price: {self.price}\n'\
               f'store: {self.store}\n'\
               f'url: {self.url}\n'

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
    
    def get_page(self, sleep_time = 0):
        with self.get_chrome() as driver:
            url = urllib.parse.quote(self.search_url, safe='?:/=&+')
            driver.get(url)
            if sleep_time:
                time.sleep(sleep_time)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            return soup

    async def scrape(self):
        pass

class Scrapers():
    def __init__(self, disc_search):
        self.norwegian =     [DiscInStock(disc_search), 
                              FrisbeeFeber(disc_search),
                              SuneSport(disc_search),
                              Xxl(disc_search)]
        self.voec =          [DiscExpress(disc_search),
                              Discconnection(disc_search),
                              Discsport(disc_search),
                              Discmania(disc_search)]
        self.international = [Latitude64(disc_search),
                              Discrepublic(disc_search)]

class DiscInStock(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search)
        self.search_url = f'https://www.discinstock.no/?name={disc_search}'
    
    def scrape(self):
        soup = self.get_page(1)

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
        self.search_url = f'https://www.frisbeefeber.no/search_result?keywords={disc_search}'
    
    def scrape(self):
        soup = self.get_page()

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
            url = product.find('a', href=True)
            disc.url = url['href']

            self.discs.append(disc) 

# Sune Sport does not contain disc manufacturer
class SuneSport(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search)
        self.url = 'sunesport.no'
        self.search_url = f'https://sunesport.no/product/search.html?search={disc_search}&category_id=268&sub_category=true'
    
    def scrape(self):
        soup = self.get_page()

        for product in soup.findAll("div", class_="product-thumb"):
            if (product.find("span", class_="stock-status").getText() == "Utsolgt"):
                continue

            disc = Disc()
            caption = product.find("div", class_="caption")
            h4 = caption.find("h4")
            a = h4.find('a', href=True)
            disc.name = a.getText()
            disc.url = a["href"]
            disc.price = re.search(r" (.*?)Ekskl.", caption.find("p", class_="price").getText()).group(1)
            disc.store = self.url
            self.discs.append(disc)

class Xxl(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search.replace(" ", "+"))
        self.url = 'xxl.no'
        self.product_url = 'https://www.xxl.no'
        self.search_url = f'https://www.xxl.no/search?query={self.disc_search}&sort=relevance&Frisbeegolffilters_string_mv=Driver&Frisbeegolffilters_string_mv=Putter&Frisbeegolffilters_string_mv=Mid+range+frisbee'
    
    def scrape(self):
        soup = self.get_page(1)

        contain_discs = False

        for filter in soup.findAll("div", class_="MuiAccordionSummary-content jss11 Mui-expanded jss12"):
            if "Frisbeegolf" in filter.getText():
                contain_discs = True

        if (contain_discs == False):
            return

        product_list = soup.find("ul", class_="product-list product-list--multiline")
        for product in product_list.findAll("li"):                
            product_info = product.find("div", class_="product-card__info-wrapper")
            name = product_info.find("p").getText().split(", ")[0]
            # Must check since xxl.no returns false results
            if (self.disc_search.lower() not in name.lower()):
                continue
            disc = Disc()
            disc.name = product_info.find("p").getText().split(", ")[0]
            disc.manufacturer = product_info.find("h3").getText()
            product_price = product.find("div", class_="product-card__price-wrapper")                
            disc.price = product_price.find("p").getText()
            a = product.find('a', href=True)
            disc.url = f'{self.product_url}{a["href"]}'
            disc.store = self.url
            self.discs.append(disc)

# Discexpress does not contain disc manufacturer
class DiscExpress(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search)
        self.url = 'discexpress.se'
        self.url_product = 'https://www.discexpress.se'
        self.search_url = f'https://www.discexpress.se/a/search?type=product&q={disc_search}'
    
    def scrape(self):
        soup = self.get_page()

        for grid_item in soup.findAll("div", class_="grid-item search-result large--one-fifth medium--one-third small--one-half"):
            if (self.disc_search.lower() not in grid_item.find("p").getText().lower()): # Search engine gives false response
                continue

            disc = Disc()
            disc.name = grid_item.find("p").getText()
            a = grid_item.find('a', href=True)
            disc.url = f'{self.url_product}{a["href"]}'
            for hidden_item in grid_item.findAll("span", class_="visually-hidden"):
                if("kr" in hidden_item.getText().lower()):
                    disc.price = hidden_item.getText()                 
            disc.store = self.url
            self.discs.append(disc)

class Discconnection(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search)
        self.url = 'discconnection.dk'
        self.search_url = f'https://discconnection.dk/default.asp?page=productlist.asp&Search_Hovedgruppe=&Search_Undergruppe=&Search_Producent=&Search_Type=&Search_Model=&Search_Plastic=&PriceFrom=&PriceTo=&Search_FREE={disc_search}'
    
    def scrape(self):
        soup = self.get_page()
            
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
            disc.url = self.search_url
            self.discs.append(disc)

class Discsport(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search)
        self.url = 'discsport.se'
        self.search_url = f'https://discsport.se/shopping/?search_adv=&name={disc_search}&selBrand=0&selCat=1&selType=0&selStatus=0&selMold=0&selDiscType=0&selStability=0&selPlastic=0&selPlasticQuality=0&selColSel=0&selColPrim=0&selCol=0&selWeightInt=0&selWeight=0&sel_speed=0&sel_glide=0&sel_turn=-100&sel_fade=-100&Submit='
    
    def scrape(self):
        soup = self.get_page()

        products = soup.find('ul', class_="products")
        if (products is not None):
            for product in products.findAll("li"):
                if product.find("div", class_="upperLeftLabel"): # Not in stock
                    continue
                disc = Disc()
                a = product.find("h3", class_="shop_item").find('a', href=True)
                disc.name = a.getText().replace("\n", " ").replace("\t", " ")
                disc.url = a["href"]
                manufacturer = re.search(r"]<br/>(.*?)\|", a["title"]).group(1).replace("\xa0", "")
                if (manufacturer is not None):
                    disc.manufacturer = manufacturer                    
                disc.price = product.find("div", class_="text-center").find("p").getText()
                disc.store = self.url
                self.discs.append(disc)

class Discmania(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search)
        self.url = 'discmania.net'
        self.url_product = 'https://europe.discmania.net'
        self.search_url = f'https://europe.discmania.net/search?type=product%2Carticle%2Cpage&q={disc_search}'
    
    def scrape(self):
        soup = self.get_page()

        for product in soup.findAll("div", class_="o-layout__item u-1/1 u-1/2@phab u-1/4@tab"):
            name = product.find("h3", class_= "product__title h4").getText()

            if self.disc_search.lower() not in name.lower(): # Gives some false products
                continue

            disc = Disc()
            disc.name = name
            disc.manufacturer = product.find("h4", class_= "product__vendor h6").getText()
            a = product.find("a", class_="product-link", href=True)
            disc.url = f'{self.url_product}{a["href"]}'
            disc.price = product.find("span", class_="money").getText()
            disc.store = self.url
            self.discs.append(disc)

# Latitude64
class Latitude64(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search)
        self.url = 'store.latitude64.se'
        self.url_product = 'https://store.latitude64.se/'
        self.search_url = f'https://store.latitude64.se/search?q={disc_search}'
    
    def scrape(self):
        soup = self.get_page(1)

        for prodHeader in soup.findAll("div", class_="box product"):
            title =  prodHeader.find("a", class_="title")
            if (title is None):
                continue
            disc = Disc()
            disc.name = title.getText()
            disc.url = f'{self.url_product}{title["href"]}'
            disc.manufacturer = prodHeader.find("span", class_="vendor").getText()
            disc.price = prodHeader.find("span", class_="money").getText()
            disc.store = self.url
            self.discs.append(disc)

# DiscRepublic
class Discrepublic(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search)
        self.url = 'discrepublic.ca'
        self.url_product = 'https://discrepublic.ca'
        self.search_url = f'https://discrepublic.ca/search?type=product&collection=in-stock&q=*{disc_search}*'
    
    def scrape(self):
        soup = self.get_page(1)

        # Check if the disc is sold out
        for product in soup.findAll("div", class_="product-item-wrapper col-sm-2"):
            if product.find("span", class_="sold_out"):
                continue

            # mold contain the disc name, must check this field
            mold = product.find("span", class_="mold").getText()
            plastic = product.find("span", class_="plastic")
            # Is the product a disc?
            if plastic is None:
                continue                
            if self.disc_search.lower() not in f'{mold.lower()} {plastic.getText().lower()}':
                continue

            disc = Disc()
            disc.name = f'{mold} {plastic.getText()}'
            product_title = product.find("div", class_="product-title")                
            title = product_title.find('a', href=True)
            # manufacturer is fetched from an alt string
            img = product.find('img', class_="not-rotation img-responsive front")
            disc.manufacturer = img["alt"].split(" ")[0]
            disc.url = f'{self.url_product}{title["href"]}'

            # If the disc is on sale, there is two prices. Check and use correct
            normal_price = product.find("span", class_="price_sale price_normal")
            if normal_price is None:
                disc.price = product.find("span", class_="price_sale").getText().replace("\n", "")
            else:
                disc.price = normal_price.getText().replace("\n", "")
            disc.store = self.url                

            self.discs.append(disc)

# MarshallStreet, fetches flight info
class MarshallStreetFlight(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search)
        self.search_url = f'https://www.marshallstreetdiscgolf.com/flightguide'

    def scrape(self):
        soup = self.get_page()
        for disc_item in soup.findAll("div", class_="flex-grid-item disc-item"):
            if (disc_item.getText().lower() == self.disc_search.lower()):
                disc = Disc()
                disc.name = disc_item.getText()
                disc.img_url = disc_item['data-pic']
                disc.speed = disc_item['data-speed']
                disc.glide = disc_item['data-glide']
                disc.turn = disc_item['data-turn']
                disc.fade = disc_item['data-fade']
                self.discs.append(disc)
                return
        for putter in soup.findAll("div", class_="putter-child pc-entry"):
            putter_name = putter['data-putter']
            if (putter_name.lower() == self.disc_search.lower()):
                disc = Disc()
                disc.name = putter_name
                disc.img_url = putter['data-image']
                disc.speed = putter['data-speed']
                disc.glide = putter['data-glide']
                disc.turn = putter['data-turn']
                disc.fade = putter['data-fade']
                self.discs.append(disc)
                return       

class RocketDiscs(Scraper):
    def __init__(self, disc_search):
        super().__init__(disc_search)
        self.url = 'https://rocketdiscs.com/'
        self.url_product = 'https://rocketdiscs.com'
        self.search_url = 'https://rocketdiscs.com/Disc-Matrix'
    
    def get_page_source(self, driver, url):
        url = urllib.parse.quote(url, safe='?:/=&')
        driver.get(url)
        time.sleep(3)
        content = driver.page_source
        return content
    
    def get_disc_from_matrix(self, driver):
        content = self.get_page_source(driver, self.search_url)
        soup = BeautifulSoup(content, "html.parser")
        disc = re.compile(f'.*{self.disc_search}.*', re.IGNORECASE)
        product = soup.find("a", title=disc)
        self.manufaturer = product["href"].split("-")[0][1:]
        self.url_product += product["href"]
        
    def scrape(self):
        with self.get_chrome() as driver:
            self.get_disc_from_matrix(driver)
            
            # Find disc in product page and scrape
            content = self.get_page_source(driver, self.url_product)
            soup = BeautifulSoup(content, "html.parser")
            # Check if there is an Out of stock banner
            if soup.find("div", id="ContentPlaceHolder1_bannerText") == None:
                print(f'Found disc in stock!')
                name = soup.find("h1", id="ContentPlaceHolder1_lblDiscName").text
                price = soup.find("td", id="ContentPlaceHolder1_lblOurPrice").text
                
                disc = Disc()
                disc.name = name
                disc.url = f'{self.url_product}'
                disc.manufacturer = self.manufaturer
                disc.price = price
                disc.store = self.url
                print(disc)
                self.discs.append(disc)
