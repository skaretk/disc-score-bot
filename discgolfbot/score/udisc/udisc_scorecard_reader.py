import csv
import datetime
from pathlib import Path
from score.player import Player
from .udisc_scorecard import UdiscScorecard
from .udisc_scorecard_old import UdiscScoreCardOld
from .udisc_csv_types import UdiscCsvTypes

udisc_scorecard_header = ["PlayerName", "CourseName", "LayoutName", "StartDate", "EndDate", "Total", "+/-", "RoundRating", "Hole"]
udisc_scorecard_header_old = ["PlayerName", "CourseName", "LayoutName", "Date", "Total", "+/-", "Hole"]

class UdiscScoreCardReader:
    """uDisc Scorecard reader for uDisc .csv files"""
    def __init__(self, file:Path, csv_type:UdiscCsvTypes):
        self.file = file
        self.csv_type = csv_type

    def parse(self):
        """Parse and return the Udisc Scorecard"""
        with open(self.file, encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if reader.line_num == 2:
                    if self.csv_type == UdiscCsvTypes.SCORECARD:
                        scorecard = UdiscScorecard()
                        scorecard.date_time = row['StartDate']
                        scorecard.date_time_end = row['EndDate']
                    elif self.csv_type == UdiscCsvTypes.SCORECARD_OLD:
                        scorecard = UdiscScoreCardOld()
                        scorecard.date_time = row['Date']
                    else:
                        return None

                    scorecard.course.name = row['CourseName']
                    scorecard.course.layout = row['LayoutName']
                    scorecard.par = int(row['Total'])
                    for i in range(1, 28):
                        if f'Hole{i}' in row:
                            scorecard.add_hole(i, int(row[f'Hole{i}']))
                        else:
                            break
                else:
                    player = Player(row['PlayerName'], int(row['Total']), int(row['+/-']))
                    if self.csv_type == UdiscCsvTypes.SCORECARD:
                        player.rating = int(row['RoundRating'])
                    for i in range(0, len(scorecard.holes)):
                        score = int(row[f'Hole{i+1}'])
                        player.add_hole(score)
                        player.player_stats.add_score(score, scorecard.holes[i+1])
                    scorecard.add_player(player)
        return scorecard

    def contain_course(self, course):
        """Check if the scorecard is course"""
        with open(self.file, encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if reader.line_num == 2:
                    add_scorecard = course.lower() in row['CourseName'].lower()
                    break

        if add_scorecard:
            return self.parse()
        return None

    def contain_dates(self, date:datetime, date_to:datetime):
        """Check if the given scorecard is within the dates"""
        with open(self.file, encoding='UTF-8', newline='') as csv_file:
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
