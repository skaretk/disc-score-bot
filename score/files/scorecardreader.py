import csv
import datetime
from score.player import Player
from score.player import PlayerName
from score.scorecard import Scorecard

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
                        try:
                            if row[f'Hole{i}'] is not None:
                                scorecard.add_hole(i, int(row[f'Hole{i}']))
                        except:
                            break 
                else:
                    player = Player(PlayerName(row['PlayerName']), int(row['Total']), int(row['+/-']))
                    for i in range(0, len(scorecard.holes)):
                        player.add_hole(int(row[f'Hole{i+1}']))
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
