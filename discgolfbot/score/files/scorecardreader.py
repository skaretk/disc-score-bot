import csv
import datetime
from score.player import Player
from score.player import PlayerName
from score.scorecard import Scorecard
from score.statistics import Statistics

def get_golf_score(statistics:Statistics, score, par):
    if (score == 1):
        statistics.ace += 1
    elif (score == par-4):
        statistics.kondor += 1
    elif (score == par-3):
        statistics.albatross += 1
    elif (score == par-2):
        statistics.eagle += 1
    elif (score == par-1):
        statistics.birdie += 1
    elif (score == par):
        statistics.par += 1
    elif (score == par+1):
        statistics.bogey += 1
    elif (score == par+2):
        statistics.double_bogey += 1
    elif (score >= par+3):
        statistics.triple_bogey_plus += 1

class ScorecardReader:
    def __init__(self, path, file):
        self.path = path
        self.file = file
    
    def parse(self):
        with open(f'{self.path}\{self.file}', encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if reader.line_num == 2:
                    scorecard = Scorecard(row['CourseName'], row['LayoutName'], row['Date'], int(row['Total']))
                    for i in range(1, 28):
                        if f'Hole{i}' in row:
                                scorecard.add_hole(i, int(row[f'Hole{i}']))
                        else:
                            break 
                else:
                    player = Player(PlayerName(row['PlayerName']), int(row['Total']), int(row['+/-']))
                    for i in range(0, len(scorecard.holes)):
                        score = int(row[f'Hole{i+1}'])
                        player.add_hole(score)
                        get_golf_score(player.player_stats, score, scorecard.holes[i+1])
                    scorecard.add_player(player)
        return scorecard
    
    def parse_course(self, course):
        with open(f'{self.path}\{self.file}', encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if reader.line_num == 2:
                    if course.lower() in row['CourseName'].lower():
                        scorecard = Scorecard(row['CourseName'], row['LayoutName'], row['Date'], int(row['Total']) )
                    else:
                        return None
                else:
                    player = Player(PlayerName(row['PlayerName']), int(row['Total']), int(row['+/-']))
                    scorecard.add_player(player)
        return scorecard

    def parse_dates(self, date, date_to = ''):
        with open(f'{self.path}\{self.file}', encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if reader.line_num == 2:                  
                    scorecard_date = datetime.datetime.strptime(row['Date'],'%Y-%m-%d %H:%M')
                    # Parse scores between two dates ?
                    if (date_to):
                        if date.date() <= scorecard_date.date() and date_to.date() >= scorecard_date.date():
                            add_scorecard = True
                        else:
                            add_scorecard = False
                    # Only one date
                    else:
                        if date.date() == scorecard_date.date():
                            add_scorecard = True
                        else:
                            add_scorecard = False
                    
                    if (add_scorecard):
                        scorecard = Scorecard(row['CourseName'], row['LayoutName'], row['Date'], int(row['Total']) )
                    else:
                        return None
                else:
                    player = Player(PlayerName(row['PlayerName']), int(row['Total']), int(row['+/-']))
                    scorecard.add_player(player)
        return scorecard
