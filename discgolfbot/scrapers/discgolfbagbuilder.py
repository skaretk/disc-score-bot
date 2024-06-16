import time
from disc.disc import Disc
from selenium.webdriver.common.by import By
from .scraper import Scraper

# DiscgolfBagBuilder does not contain disc manufacturer
class DiscgolfBagBuilder(Scraper):
    """Discgolfbagbuilder Scraper, scrapes bag"""
    def __init__(self, url):
        super().__init__()
        self.name = 'discgolfbagbuilder.com'
        self.url = 'https://www.discgolfbagbuilder.com'
        self.scrape_url = url
        self.bag_name = "Bag"
        self.bag_description = ""
        self.icon_url = 'https://pbs.twimg.com/profile_images/1298004778224619520/XfPTj4i1.jpg'
        self.image_file = "flight.png"
        self.distance_drivers = None
        self.fairway_drivers = None
        self.midranges = None
        self.putt_approach = None

    def scrape_discs(self):
        """Scrape discs from the bag"""
        start_time = time.time()
        soup, driver = self.selenium_get_beatifulsoup_and_chromedriver()
        # add cookie in order to get meters instead of feet
        driver.add_cookie({"name": "measurement_unit", "value": "meters"})
        driver.refresh()

        element = driver.find_element(By.CLASS_NAME, "y_axis")
        element.screenshot(self.image_file)
        driver.close()

        meta_properties = soup.find_all("meta", property=True)
        for meta_property in meta_properties:
            if meta_property["property"] is not None:
                if meta_property["property"] == "og:title": # Contains bag name
                    self.bag_name = meta_property["content"]
                elif meta_property["property"] == "og:description":
                    self.bag_description = meta_property["content"]

        categories = soup.find_all("h2", {"class":"text-xl"})
        discs = soup.find_all("div", {"class":"grid-cols-1"})

        for i, category in enumerate(categories):
            discs_list = []
            discs_div = discs[i].find_all("div", {"class":"flex-row"})

            for disc_div in discs_div:
                disc = Disc()

                disc_element = disc_div.find("a")

                # Disc name
                disc_text = disc_element.getText()
                if "(" in disc_text:
                    text_array = disc_text.split('(')
                    disc.name = text_array[0]
                    if len(text_array) == 2:
                        disc.info = text_array[1].replace(")", "")
                    elif len(text_array) == 3:
                        disc.info = f'{text_array[1]}{text_array[2]}'.replace(")", "")
                else:
                    disc.name = disc_text

                # Disc url
                disc_url = disc_element['href']
                if disc_url is not None:
                    disc.url = f'{self.url}{disc_url}'

                # Disc flight numbers
                flight = disc_div.find("div", {"class":"text-right"}).text.split("/")
                flight = list(map(str.strip, flight))
                if len(flight) == 4: # Make sure we have all flight numbers
                    disc.speed = flight[0]
                    disc.glide = flight[1]
                    disc.turn = flight[2]
                    disc.fade = flight[3]
                discs_list.append(disc)

            if category.getText() == "Distance Driver":
                self.distance_drivers = discs_list
            elif category.getText() == "Fairway Driver":
                self.fairway_drivers = discs_list
            elif category.getText() == "Midrange":
                self.midranges = discs_list
            elif category.getText() == "Putt Approach":
                self.putt_approach = discs_list
            else:
                print(f'Unknown category {category.getText()}')

        self.scraper_time = time.time() - start_time
        print(f'DiscgolfBagBuilder scraper: {self.scraper_time}')
