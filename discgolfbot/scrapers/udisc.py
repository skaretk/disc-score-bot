import time
from dateutil.parser import parse
from score.scorecard import Scorecard
from score.player import Player, PlayerName
from .scraper import Scraper

class Udisc(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'udisc.com'
        self.url = 'https://udisc.com'

class LeagueScraper(Udisc):
    def __init__(self, url):
        super().__init__()
        self.scrape_url = url
        self.score_card = Scorecard("", "", "2021-01-01 12:00", 0)
        
    def scrape(self):
        start_time = time.time()

        soup = self.selenium_get_beatifulsoup(4)

        header = soup.find("div", class_="jss39 jss41")
        if header is None:
            return        

        # Course Name
        course_name = header.find("a", class_="MuiTypography-root MuiLink-root MuiLink-underlineHover jss101 MuiTypography-colorPrimary")
        if course_name is None:
            return
        self.score_card.coursename = course_name.getText().rstrip()
        # Course link
        course_url = course_name['href']
        if course_url is not None:
            self.score_card.course_url = f'{self.url}{course_url}'

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
        # Add par for holes
        hole_par_list = tour_id.find_all("p", class_="jss146 jss182")
        for i in range(len(hole_par_list)):
            self.score_card.add_hole(i+1, int(hole_par_list[i].getText()))

        # Add players and scores
        for player in tour_id.find_all("tr", class_="jss148 false collapsed"):
            player_name = PlayerName("")
            score = ""
            scores = []
            player_row = player.find_all("td", class_="jss150 jss183")
            for row_no in range(len(player_row)):
                if(row_no == 0):
                    player_name.name = player_row[row_no].getText()
                elif (row_no == 1):
                    if (player_row[row_no].getText() == "E"):
                        score = "0"
                    else:
                        score = player_row[row_no].getText().replace("+", "")
                elif(row_no > 2):
                    scores.append(player_row[row_no].getText())

            total = scores.pop()
            scorecard_player = Player(player_name, total, score)
            for hole_score in scores:
                scorecard_player.add_hole(hole_score)
            self.score_card.add_player(scorecard_player)
        
        self.scraper_time = time.time() - start_time
        print(f'UdiscLeague scraper: {self.scraper_time}')
