import time
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
        self.scorecard = Scorecard()

    def scrape(self):
        start_time = time.time()

        soup = self.selenium_get_beatifulsoup(5)

        header = soup.find("div", {"class" : ["jss55", "jss57"]})
        if header is None:
            return

        # Course Name
        course_name = header.find("a", {"class" : "jss75"})
        if course_name is None:
            return
        self.scorecard.course.name = course_name.getText().rstrip()
        # Course url
        course_url = course_name['href']
        if course_url is not None:
            self.scorecard.course.url = f'{self.url}{course_url}'

        # Layout Name
        self.scorecard.course.layout = soup.find("p", {"class" : "jss96"}).getText().replace("LAYOUT: ", "").rstrip(" ")

        date = header.find("p", {"class" : "jss74"})
        if date is None:
            return
        # Date, varies between two formats ("September 12th 2021, or "Sept 12")
        date = date.getText().split("·")[1].rstrip().lstrip()
        self.scorecard.date_time = date

        divisions_list = []
        divisions = soup.find_all("p", {"class" : "jss77"})
        for division in divisions:
            divisions_list.append(division.getText().split()[0]) # Only fetch the first word)

        #tour_id = soup.find("div", id="tour-leaderboard")
        tour_id = soup.find("div", {"id" : "tour-leaderboard"})
        par_list = tour_id.find_all("p", {"class" : ["jss122", "jss158"]})
        for i, par in enumerate(par_list):
            if par == par_list[-1]: # Last element is par
                self.scorecard.par = int(par.getText())
            else:
                self.scorecard.add_hole(i+1, int(par.getText()))

        division_scores = soup.findAll("div", {"class" : "jss113"} )
        for i, division_score in enumerate(division_scores):
            for player in division_score.find_all("tr", {"class" : ["jss126", "false"]}):
                player_name = PlayerName("")
                score = ""
                scores = []
                player_rows = player.find_all("td", {"class" : "jss126"})

                for row_no, player_row in enumerate(player_rows):
                    if row_no == 1:
                        player_name.name = player_row.getText()
                    elif row_no == 2:
                        if player_row.getText() == "E":
                            score = "0"
                        else:
                            score = player_row.getText().replace("+", "")
                    elif row_no > 3:
                        scores.append(player_row.getText())

                total = scores.pop() # last element is the total
                scorecard_player = Player(player_name, total, score)
                scorecard_player.division = divisions_list[i]
                for hole_score in scores:
                    scorecard_player.add_hole(hole_score)
                self.scorecard.add_player(scorecard_player)

        self.scraper_time = time.time() - start_time
        print(f'UdiscLeague scraper: {self.scraper_time}')
