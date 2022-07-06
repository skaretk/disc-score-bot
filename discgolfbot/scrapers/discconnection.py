import time
from discs.disc import Disc
from .scraper import Scraper

class Discconnection(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'discconnection.dk'
        self.url = 'https://discconnection.dk'

class DiscScraper(Discconnection):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://discconnection.dk/default.asp?page=productlist.asp&Search_Hovedgruppe=&Search_Undergruppe=&Search_Producent=&Search_Type=&Search_Model=&Search_Plastic=&PriceFrom=&PriceTo=&Search_FREE={search}'
        self.discs = []
        self.valid_categories = ["Andre discs", "Brugte discs", "Collectors discs", "Golf discs"]

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_get_beatifulsoup()

        names = []
        manufacturers = []
        prices = []
        images = []

        categories = soup.findAll("div", class_="bigText")
        product_list = soup.findAll("table", class_="productlist")

        for idx, category in enumerate(categories):
            valid = any(category.getText() in string for string in self.valid_categories)
            if (valid == False):
                continue

            # Contains: "Innova Firebird  •  Plastic: Champion  •  Driver"
            for prodHeader in product_list[idx].findAll("td", class_="prodHeader"):
                text = prodHeader.getText().replace("\xa0", "").split("•")
                manufacturer = text[0].split()[0]
                manufacturers.append(manufacturer)
                names.append(f'{text[0]} - {text[1].replace("Plastic: ", "")}')

            # Contains: Pris inkl. moms: 120,00 DKK
            for prodPriceWeight in product_list[idx].findAll("td", class_="prodPriceWeight"):
                if prodPriceWeight.has_attr("align"):
                    continue
                b = prodPriceWeight.find("b")
                if b is not None:
                    prices.append(b.getText())
                else:
                    # Discounted price? Contains: TILBUD: 300 - spar 50 DKK
                    discount = prodPriceWeight.find("div", class_="discount")
                    if discount is not None:
                        price = discount.getText().split()
                        prices.append(f'{price[1]} DKK')

            for discImage in product_list[idx].findAll("img"):
                images.append(discImage["src"])


        for i in range(len(names)):
            disc = Disc()
            disc.name = names[i]
            disc.manufacturer = manufacturers[i]
            disc.price = prices[i]
            disc.store = self.name
            disc.img = images[i]
            disc.url = self.scrape_url
            self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'Discconnection scraper: {self.scraper_time}')
