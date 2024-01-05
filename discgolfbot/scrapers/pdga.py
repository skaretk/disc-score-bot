import time
from discs.disc import PdgaApprovedDisc
from .scraper import Scraper
import re

class Pdga(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'PDGA Approved Disc Golf Discs'
        self.url = 'https://www.pdga.com/'

class DiscScraper(Pdga):
    def __init__(self):
        super().__init__()
        self.scrape_url = f'https://www.pdga.com/technical-standards/equipment-certification/discs'
        self.discs = []
    
    def scrape(self):
        start_time = time.time()
        soup = self.urllib_header_get_beatifulsoup()

        manufacturers = soup.findAll("td", class_="views-field views-field-field-equipment-manuf-ref")
        disc_models = soup.findAll("td", class_="views-field views-field-title")
        approved_dates = soup.findAll("td", class_="views-field views-field-field-equipment-approve-date")

        for idx, disc_model in enumerate(disc_models):
            approved_disc = PdgaApprovedDisc()
            # Fetch Manufacturer
            manufacturer = manufacturers[idx].getText()
            approved_disc.manufacturer = manufacturer.replace("\n", "").lstrip().rstrip()
            # Fetch Disc Model
            disc_model = disc_models[idx].getText()
            approved_disc.name = disc_model.replace("\n", "").lstrip().rstrip()
            # Fetch Approved Date
            approved_date = approved_dates[idx].getText()
            approved_disc.approved_date = approved_date.replace("\n", "").lstrip().rstrip()
            # Fetch link
            a = disc_models[idx].find('a', href=True)
            url = f'{self.url}{a["href"]}'
            approved_disc.url = url
            # Append
            self.discs.append(approved_disc)

        self.scraper_time = time.time() - start_time
        print(f'PDGA scraper: {self.scraper_time}')

class PdgaPlayerData():
    def __init__(self, pdga_number):
        self.pdga_number = pdga_number
        self.current_rating = 0
        self.rating_change = 0
        self.location = ''
        self.membership_status = ''
        self.offical_status = ''
        self.career_events = 0 
        self.upcoming_events = ''
        self.portrait_url = ''
        self.player_name = ''

    def generate_dict(self): # finnes det noen bedre måter å gjøre dette på?
        return {
            "Current Rating": self.current_rating,
            "Career Events": self.career_events,
            "Location": self.location,
            "Membership Status": self.membership_status,
            "Official Status": self.offical_status,
            "PDGA Number": self.pdga_number,
            "Ratings Change": self.rating_change,
            "Upcoming Events": self.upcoming_events,
        }


class PlayerProfileScraper(Pdga):
    def __init__(self, pdga_number):
        super().__init__()
        self.name = "PDGA Player Profile"
        self.scrape_url = 'https://www.pdga.com/player/' + pdga_number
        self.pdga_number = pdga_number
        self.player_data = PdgaPlayerData(pdga_number=self.pdga_number)
        self.player_data_dict = {}

    def scrape(self):
        start_time = time.time()
        
        # headers
        headers = {
            "Host": "www.pdga.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "no,en;q=0.7,en-US;q=0.3",
            "Accept-Encoding": "*",
        }
        self.soup = self.urllib_header_get_beatifulsoup(headers=headers)
        
        # find the location data of the player
        loc_obj = self.soup.find_all('li', 'location')    
        self.player_data.location = loc_obj[0].a.text   
        # find the membership status of the player
        membership_obj = self.soup.find_all('li', 'membership-status')
        self.player_data.membership_status = membership_obj[0].text.split(": ")[-1].lstrip().rstrip()
        # find the rules official status of the player
        self.find_official_data()
        
        # retrieve the player current rating
        self.find_current_rating()

        # find the rating difference gain
        self.find_rating_difference_gain()

        # try to find player portrait data (url and player name)
        player_portrait_data = self.get_player_portrait_data()

        if player_portrait_data:
            # assign the player name from the portrait data
            self.player_data.player_name = player_portrait_data['alt'].split(self.player_data.pdga_number)[0].lstrip().rstrip() 
        else:
            # assign the player name from the meta tag
            self.find_player_name(tag="meta", tag_property="og:title")

        # parse players upcoming event and assemble a string worthy of discord-embeds :)
        self.get_player_upcoming_events_data()

        # find the past events data
        self.get_singles_event_history()
        
        # print the chore
        self.scraper_time = time.time() - start_time
        print(f'PDGA scraper: {self.scraper_time}')
        
        # set player data dict - so we have something to test
        self.player_data_dict = self.player_data.generate_dict()
    

    def find_player_name(self, tag="meta", tag_property="og:title"):
        player_name = '-'
        player_name_metadata = self.soup.find(name=tag, property=tag_property)
        if 'content' in player_name_metadata.attrs:
            player_name = player_name_metadata.attrs['content'].split("#")[0].rstrip()
        self.player_data.player_name = player_name
    
    def find_current_rating(self):
        current_rating_data = None
        current_rating_data = self.soup.find('li', 'current-rating')
        if None == current_rating_data:
            self.player_data.current_rating = 'n/a'
            return
        self.player_data.current_rating = current_rating_data.text.split(": ")[-1].lstrip().rstrip()


    def find_rating_difference_gain(self):
        rating_diff_data = self.soup.find_all(name='a', property='rating-difference gain')
        if len(rating_diff_data) == 0:
            self.player_data.rating_change = 'n/a'
            return
        rating_diff_data[0].find_all(name='a', property='rating-difference gain')[0].text
        self.player_data.rating_change = rating_diff_data[0].find_all(name='a', property='rating-difference gain')[0].text

    def get_singles_event_history(self):
        singles_events_obj = self.soup.find_all('li', 'career-events disclaimer')
        if len(singles_events_obj) == 0:
            self.player_data.career_events = '0'
            return
        self.player_data.career_events = singles_events_obj[0].text.split(": ")[-1]

    def get_player_portrait_data(self):
        try:
            player_portrait_data = None
            regex_compile = re.compile(pattern=f"\w+\s{self.player_data.pdga_number}")
            port_data = self.soup.find_all('img')
            for pd in port_data:
                regex_compile.findall(pd.attrs['alt'])
                if regex_compile.search(string=pd.attrs['alt']):
                    player_portrait_data = pd.attrs.copy()
            self.player_data.portrait_url = player_portrait_data['src']
        except:
            self.player_data.portrait_url = None
            return None
        # return player_portrait_data
        return player_portrait_data
        
    
    def get_player_upcoming_events_data(self):
        try:
            # find all upcoming events
            upcoming_events_obj = self.soup.find_all("li", "upcoming-events")
            if len(upcoming_events_obj) == 0:
                # if no upcoming events, player might have 0 or just 1 upcoming event, aka next-event
                upcoming_events_obj = self.soup.find_all("li", "next-event")
                player_upcoming_events = "```yaml\n"
            if len(upcoming_events_obj) >= 1:
                for event in upcoming_events_obj[0].find_all('a'):
                    event_and_date = event['title'].split(",  on")
                    player_upcoming_events += "\n - " + event_and_date[0].replace("-",",") .lstrip().rstrip() + " " + event_and_date[1].replace("-", " ").lstrip().rstrip() #event['title'] + " \n"
            else:
                player_upcoming_events += 'No upcoming events found'
            player_upcoming_events +="\n```"
        except:
            player_upcoming_events = "```yaml\nFailed to retrieve upcoming events\n```"
        # assign player data to player_data attrs
        self.player_data.upcoming_events = player_upcoming_events


    def find_official_data(self):
        official_obj = self.soup.find_all('li', 'official')
        if len(official_obj) >= 1:
            self.player_data.offical_status = official_obj[0].text.split(": ")[-1].lstrip().rstrip()
            return
        self.player_data.offical_status = 'n/a'