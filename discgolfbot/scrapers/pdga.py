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

    def prettify(self): # bør renames til __to_dict__
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
        
class PlayerScraper(Pdga):
    def __init__(self, pdga_number):
        super().__init__()
        self.name = "www.pdga.com player information"
        self.scrape_url = 'https://www.pdga.com/player/' + pdga_number
        self.pdga_number = pdga_number
        self.player_data = PdgaPlayerData(pdga_number=pdga_number)

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
        soup = self.urllib_header_get_beatifulsoup(headers=headers)
        
        # set up soup-objects for parsing/verification
        cr_obj=soup.find_all('li', 'current-rating')
        # find all upcoming events
        upcoming_events_obj = soup.find_all("li", "upcoming-events")
        if len(upcoming_events_obj) == 0:
            # if no upcoming events, player might have 0 or just 1 upcoming event, aka next-event
            upcoming_events_obj = soup.find_all("li", "next-event")
        # find the location data of the player
        loc_obj = soup.find_all('li', 'location')       
        # find the membership status of the player
        membership_obj = soup.find_all('li', 'membership-status')
        # find the rules official status of the player
        official_obj = soup.find_all('li', 'official')
        singles_events_obj = soup.find_all('li', 'career-events disclaimer')
        
        # try to find player portrait data (url and player name)
        player_portrait_data = None
        regex_compile = re.compile(pattern=f"\w+\s{self.player_data.pdga_number}")
        port_data = soup.find_all('img')
        for pd in port_data:
            regex_compile.findall(pd.attrs['alt'])
            if regex_compile.search(string=pd.attrs['alt']):
                player_portrait_data = pd.attrs.copy()

        # parse players upcoming event and assemble a string worthy of discord-embeds :)
        player_upcoming_events = "```yaml\n"
        if len(upcoming_events_obj) >= 1:
            for event in upcoming_events_obj[0].find_all('a'):
                event_and_date = event['title'].split(",  on")
                player_upcoming_events += "\n - " + event_and_date[0].replace("-",",") .lstrip().rstrip() + " " + event_and_date[1].replace("-", " ").lstrip().rstrip() #event['title'] + " \n"
        else:
            player_upcoming_events += 'No upcoming events found'
        player_upcoming_events +="\n```"
        
        # assign player data to player_data attrs 
        self.player_data.upcoming_events = player_upcoming_events
        self.player_data.current_rating =  cr_obj[0].text.split(": ")[-1].lstrip().rstrip() 
        self.player_data.career_events = singles_events_obj[0].text.split(": ")[-1]
        self.player_data.location = loc_obj[0].a.text
        self.player_data.membership_status = membership_obj[0].text.split(": ")[-1].lstrip().rstrip()
        self.player_data.rating_change = cr_obj[0].find_all('a', 'rating-difference gain')[0].text
        self.player_data.offical_status = official_obj[0].text.split(": ")[-1].lstrip().rstrip()
        self.player_data.portrait_url = player_portrait_data['src']
        self.player_data.player_name = player_portrait_data['alt'].split(self.player_data.pdga_number)[0].lstrip().rstrip() 

        # print the chore
        self.scraper_time = time.time() - start_time
        print(f'PDGA scraper: {self.scraper_time}')
        
        #return player_data
        return self.player_data