import time
from web.scraper import Scraper
from discs.disc import DiscShop

class Discconnection(Scraper):
    def __init__(self, search):
        super().__init__(search)
        self.url = 'discconnection.dk'

class DiscScraper(Discconnection):
    def __init__(self, search):
        super().__init__(search)
        self.search_url = f'https://discconnection.dk/default.asp?page=productlist.asp&Search_Hovedgruppe=&Search_Undergruppe=&Search_Producent=&Search_Type=&Search_Model=&Search_Plastic=&PriceFrom=&PriceTo=&Search_FREE={search}'
    
    def scrape(self):
        start_time = time.time()
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
            disc = DiscShop()
            disc.name = names[i]
            disc.manufacturer = manufacturers[i]
            disc.price = prices[i]
            disc.store = self.url
            disc.url = self.search_url
            self.discs.append(disc)
        self.search_time = time.time() - start_time
        print(f'Discconnection scraper: {self.get_search_time()}')
