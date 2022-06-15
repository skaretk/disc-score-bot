import time
from discs.disc import DiscBag
from .scraper import Scraper

# DiscgolfBagBuilder does not contain disc manufacturer
class DiscgolfBagBuilder(Scraper):
    def __init__(self, url):
        super().__init__()
        self.name = 'discgolfbagbuilder.com'
        self.url = 'https://www.discgolfbagbuilder.com'        
        self.scrape_url = url
        self.bag_name = "Bag"
        self.bag_description = ""
        self.icon_url = 'https://pbs.twimg.com/profile_images/1298004778224619520/XfPTj4i1.jpg'
        self.image_file = "flight.png"
        self.distance_drivers = []
        self.fairway_drivers = []
        self.midranges = []
        self.putt_approach = []
    
    def scrape_discs(self):
        start_time = time.time()
        soup, driver = self.selenium_get_beatifulsoup_and_chromedriver()
        # add cookie in order to get meters instead of feet
        driver.add_cookie({"name": "measurement_unit", "value": "meters"})
        driver.refresh()

        element = driver.find_element_by_class_name('y_axis')
        element.screenshot(self.image_file)
        driver.close()
        
        meta_properties = soup.findAll("meta", property=True)
        for property in meta_properties:
            if (property["property"] is not None):
                if (property["property"] == "og:title"): # Contains bag name
                    self.bag_name = property["content"]
                elif (property["property"] == "og:description"):
                    self.bag_description = property["content"]

        categories = soup.findAll("h2", class_="text-xl pt-6 mb-2 border-b border-gray-600")
        discs = soup.findAll("div", class_="grid grid-cols-1 gap-y-1 gap-x-4")

        for idx, category in enumerate(categories):
            # Scrape discs
            discs_list = []
            discs_div = discs[idx].findAll("div", class_="flex flex-row justify-between")
            for disc in discs_div:
                disc_bag = DiscBag()
                disc_element = disc.find("a", class_="text-indigo-600 hover:text-indigo-500 focus:outline-none focus:underline transition ease-in-out duration-150")
                disc_text = disc_element.getText()
                disc_link = disc_element['href']
                if (disc_link is not None):
                    disc_bag.url = f'{self.url}{disc_element["href"]}'
                
                if ("(" in disc_text):
                    text_array = disc_text.split('(')
                    disc_bag.name = text_array[0]
                    if len(text_array) == 2:                        
                        disc_bag.info = text_array[1].replace(")", "")
                    elif len(text_array) == 3:
                        disc_bag.info = f'{text_array[1]}{text_array[2]}'.replace(")", "")
                else:
                    disc_bag.name = disc_text
                
                flight = disc.find("div", class_="text-right").getText().split("/")
                disc_bag.speed = flight[0].rstrip().lstrip()
                disc_bag.glide = flight[1].rstrip().lstrip()
                disc_bag.turn = flight[2].rstrip().lstrip()
                disc_bag.fade = flight[3].rstrip().lstrip()
                discs_list.append(disc_bag)

            if (category.getText() == "Distance Driver"):
                self.distance_drivers.extend(discs_list)
            elif (category.getText() == "Fairway Driver"):
                self.fairway_drivers.extend(discs_list)
            elif (category.getText() == "Midrange"):
                self.midranges.extend(discs_list)
            elif (category.getText() == "Putt Approach"):
                self.putt_approach.extend(discs_list)
            else:
                print(f'Unknown category {category.getText()}')

        self.scraper_time = time.time() - start_time
        print(f'DiscgolfBagBuilder scraper: {self.scraper_time}')
