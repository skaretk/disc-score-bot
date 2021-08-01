import csv
from player import Player
from scorecard import Scorecard

class Csv_reader:
    def __init__(self, path, file):
        self.path = path
        self.file = file
    
    def parse(self):
        with open('{}\{}'.format(self.path, self.file)) as csv_file:
            reader = csv.DictReader(csv_file)
            line_count = 0
            for row in reader:
                if line_count == 0:
                    scorecard = Scorecard(row['CourseName'], row['Date'], int(row['Total']) )
                else:
                    player = Player(row['PlayerName'], int(row['Total']), int(row['+/-']))
                    scorecard.add_player(player)
                line_count += 1
            scorecard.sort_players_score()
        return scorecard