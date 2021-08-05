import csv
import datetime
from player import Player
from scorecard import Scorecard

class CsvReader:
    def __init__(self, path, file):
        self.path = path
        self.file = file       
    
    def parse(self):
        with open(f'{self.path}\{self.file}', encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            line_count = 0
            for row in reader:
                if line_count == 0:
                    scorecard = Scorecard(row['CourseName'], row['Date'], int(row['Total']) )
                else:
                    player = Player(row['PlayerName'], int(row['Total']), int(row['+/-']))
                    scorecard.add_player(player)
                line_count += 1
            scorecard.sort_players()
        return scorecard
    
    def parse_course(self, course):
        with open(f'{self.path}\{self.file}', encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            line_count = 0
            for row in reader:
                if line_count == 0:
                    if course.lower() in row['CourseName'].lower():
                        scorecard = Scorecard(row['CourseName'], row['Date'], int(row['Total']) )
                    else:
                        return None
                else:
                    player = Player(row['PlayerName'], int(row['Total']), int(row['+/-']))
                    scorecard.add_player(player)
                line_count += 1
            scorecard.sort_players()
        return scorecard

    def parse_dates(self, date, date_to = ''):
        with open(f'{self.path}\{self.file}', encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            line_count = 0
            for row in reader:
                if line_count == 0:                    
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
                        scorecard = Scorecard(row['CourseName'], row['Date'], int(row['Total']) )
                    else:
                        return None
                else:
                    player = Player(row['PlayerName'], int(row['Total']), int(row['+/-']))
                    scorecard.add_player(player)
                line_count += 1
            scorecard.sort_players()
        return scorecard
