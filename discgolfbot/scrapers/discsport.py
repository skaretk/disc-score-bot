import time
from discs.disc import Disc
from .scraper import Scraper

class Discsport(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'discsport.se'
        self.url = 'https://discsport.se'

class DiscScraper(Discsport):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://discsport.se/shopping/?search_adv=&name={search}&selBrand=0&selCat=1&selType=0&selStatus=1&selMold=0&selDiscType=0&selStability=0&selPlastic=0&selPlasticQuality=0&selColSel=0&selColPrim=0&selCol=0&selWeightInt=0&selWeight=0&sel_speed=0&sel_glide=0&sel_turn=-100&sel_fade=-100&Submit='
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_get_beatifulsoup()

        products = soup.find('div', class_="row row-cols-2 row-cols-sm-3 row-cols-md-4 row-cols-lg-5 justify-content-center g-2 g-md-3 my-4")
        if (products is not None):
            for product in products.findAll("div", class_="position-relative mx-auto text-center p-0 m-0"):
                disc = Disc()
                a = product.find("h2", class_="h5 mt-2 mb-0").find('a', href=True)
                disc.name = a.getText().replace("\n", " ").replace("\t", " ").strip()
                disc.url = a["href"]
                #manufacturer = re.search(r"]<br/>(.*?)\|", a["title"]).group(1).replace("\xa0", "")
                #if (manufacturer is not None):
                #    disc.manufacturer = manufacturer
                img = product.find("img", class_="lozad")
                if (img is not None):
                    disc.img = img["data-src"]
                disc.price = product.find("p", class_="h5 mt-1").getText().replace(':', ',')
                disc.store = self.name
                self.discs.append(disc)
        self.scraper_time = time.time() - start_time
        print(f'Discsport scraper: {self.scraper_time}')
