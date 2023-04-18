import csv
import datetime
from score.player import Player
from score.scorecard_udisc import ScorecardUdisc

udisc_scorecard_header = ["PlayerName", "CourseName", "LayoutName", "Date", "Total", "+/-", "Hole"]

class UdiscScoreCardReader:
    """uDisc Scorecard reader for uDisc .csv files"""
    def __init__(self, path="", file=""):
        self.path = path
        self.file = file

    def parse(self):
        """Parse and return the Udisc Scorecard"""
        with open(f'{self.path}/{self.file}', encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if reader.line_num == 2:
                    scorecard = ScorecardUdisc()
                    scorecard.course.name = row['CourseName']
                    scorecard.course.layout = row['LayoutName']
                    scorecard.date_time = row['Date']
                    scorecard.par = int(row['Total'])
                    for i in range(1, 28):
                        if f'Hole{i}' in row:
                            scorecard.add_hole(i, int(row[f'Hole{i}']))
                        else:
                            break
                else:
                    player = Player(row['PlayerName'], int(row['Total']), int(row['+/-']))
                    for i in range(0, len(scorecard.holes)):
                        score = int(row[f'Hole{i+1}'])
                        player.add_hole(score)
                        player.player_stats.add_score(score, scorecard.holes[i+1])
                    scorecard.add_player(player)

        return scorecard

    def contain_course(self, course):
        """Check if the scorecard is course"""
        with open(f'{self.path}/{self.file}', encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if reader.line_num == 2:
                    if course.lower() in row['CourseName'].lower():
                        add_scorecard = True
                    else:
                        add_scorecard = False

        if add_scorecard:
            return self.parse()
        return None

    def contain_dates(self, date:datetime, date_to:datetime):
        """Check if the given scorecard is within the dates"""
        with open(f'{self.path}/{self.file}', encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if reader.line_num == 2:
                    scorecard_date = datetime.datetime.strptime(row['Date'],'%Y-%m-%d %H:%M')
                    # Parse scores between two dates ?
                    if date_to:
                        add_scorecard = date.date() <= scorecard_date.date() and date_to.date() >= scorecard_date.date()
                    # Only one date
                    else:
                        add_scorecard = date.date() == scorecard_date.date()

        if add_scorecard:
            return self.parse()

        return None
