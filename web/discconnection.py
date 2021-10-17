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
        self.valid_categories = ["Andre discs", "Brugte discs", "Collectors discs", "Golf discs"]
    
    def scrape(self):
        start_time = time.time()
        soup = self.get_page()        
            
        names = []
        manufacturers = []
        prices = []

        categories = soup.findAll("div", class_="bigText")
        product_list = soup.findAll("table", class_="productlist")

        for idx, category in enumerate(categories):
            valid = any(category.getText() in string for string in self.valid_categories)
            if (valid == False):
                continue
            else:
                print(f'Found valid category {category.getText()} in index {idx}')            

            # Contains: "Innova Firebird  •  Plastic: Champion  •  Driver"
            for prodHeader in product_list[idx].findAll("td", class_="prodHeader"):
                text = prodHeader.getText().replace("\xa0", "").split("•")
                manufacturer = text[0].split()[0]
                manufacturers.append(manufacturer)
                names.append(f'{text[0]} - {text[1].replace("Plastic: ", "")}')

            # Contains: Pris inkl. moms: 120,00 DKK
            for prodPriceWeight in product_list[idx].findAll("td", class_="prodPriceWeight"):
                b = prodPriceWeight.find("b")
                if b is not None:
                    prices.append(b.getText())  
                else:
                    # Discounted price? Contains: TILBUD: 300 - spar 50 DKK
                    discount = prodPriceWeight.find("div", class_="discount")
                    if discount is not None:
                        price = discount.getText().split()
                        prices.append(f'{price[1]} DKK') 

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
