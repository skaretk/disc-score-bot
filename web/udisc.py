import time
from dateutil.parser import parse
from web.scraper import Scraper
from score.scorecard import Scorecard
from score.player import Player, PlayerName

class Udisc(Scraper):
    def __init__(self, search):
        super().__init__(search)
        self.url = 'udisc.com'

class LeagueScraper(Udisc):
    def __init__(self, url):
        super().__init__("")
        self.search_url = url
        self.score_card = Scorecard("", "", "2021-01-01 12:00", 0)
        
    def scrape(self):
        start_time = time.time()

        soup = self.get_page(4)

        header = soup.find("div", class_="jss38 jss40")
        if header is None:
            return        

        # Course Name
        course_name = header.find("a", class_="MuiTypography-root MuiLink-root MuiLink-underlineHover jss101 MuiTypography-colorPrimary")
        if course_name is None:
            return
        self.score_card.coursename = course_name.getText().rstrip()

        # Layout Name
        self.score_card.layoutname = soup.find("p", class_="MuiTypography-root jss123 MuiTypography-body1").getText().replace("LAYOUT: ", "").rstrip(" ")

        date = header.find("p", class_="MuiTypography-root jss100 MuiTypography-body1")
        if date is None:
            return
        # Date, varies between two formats ("September 12th 2021, or "Sept 12")
        date_text = date.getText().split("·")[1]
        self.score_card.date_time = parse(date_text)
        
        tour_id = soup.find("div", id="tour-leaderboard")
        # Add par
        par = tour_id.find("p", class_="jss146 jss182 undefined").getText()
        self.score_card.par = int(par)

        # Add players and scores
        for player in tour_id.find_all("tr", class_="jss148 false collapsed"):
            player_name = PlayerName("")
            total = ""
            score = ""
            scores = []
            no = 0
            for text in player.find_all("td", class_="jss150 jss183"):
                if(no == 0):
                    player_name.name = text.getText()
                elif (no == 1):
                    if (text.getText() == "E"):
                        score = "0"
                    else:
                        score = text.getText().replace("+", "")
                elif(no > 2):
                    scores.append(text.getText())
                no += 1
            total = scores.pop()
            scorecard_player = Player(player_name, total, score)
            for hole_score in scores:
                scorecard_player.add_hole(hole_score)
            self.score_card.add_player(scorecard_player)
            print(scorecard_player)
        for i in range(0, len(scorecard_player.holes)):
            self.score_card.add_hole(f'Hole{i+1}', '3')
        
        self.search_time = time.time() - start_time
        print(f'UdiscLeague scraper: {self.get_search_time()}')
