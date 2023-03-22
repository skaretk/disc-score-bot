import csv
import datetime

import dateutil.parser as dparser
from score.player import Player, PlayerName
from score.scorecard_udisc_competition import ScorecardUdiscCompetition

udisc_competition_header = ["division", "position", "name", "relative_score", "total_score", "payout"]

class UdiscCompetitionReader:
    '''uDisc Competition / League Reader'''
    def __init__(self, path, file):
        self.path = path
        self.file = file

    def parse(self):
        '''Parse the .csv file'''
        date = self.get_date()
        scorecard = ScorecardUdiscCompetition()
        scorecard.date_time = date.strftime("%Y-%m-%d %H:%M")
        scorecard.name = self.file.split('_')[0]
        with open(f'{self.path}/{self.file}', encoding='UTF-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file)

            hole_no = 1
            for field in reader.fieldnames:
                if f'hole_{hole_no}' in field:
                    scorecard.add_hole(hole_no, 0) # par is not defined in the csv
                    hole_no += 1

            for row in reader:
                if "DUP" in row['position']:
                    continue
                player = Player(PlayerName(row['name']), int(row['total_score']), int(row['relative_score']))
                player.division = row['division']
                player.score_cards_position.append(row['position'])
                for i in range(0, len(scorecard.holes)):
                    score = int(row[f'hole_{i+1}'])
                    player.add_hole(score)
                    player.player_stats.add_score(score, scorecard.holes[i+1])
                scorecard.add_player(player)
        return scorecard

    def get_date(self):
        '''Fetch date from the filename'''
        try:
            date = dparser.parse(self.file, fuzzy=True)
        except dparser.ParserError:
            date = datetime.date.today()
        return date

    def contain_course(self, course):
        '''Not possible from the csv file.'''
        return None

    def contain_dates(self, date:datetime, date_to:datetime=None):
        '''Is the scorecard within the date(s)'''
        scorecard_date = self.get_date()
        # Parse scores between two dates ?
        if date_to:
            add_scorecard = date.date() <= scorecard_date.date() and date_to.date() >= scorecard_date.date()
        # Only one date
        else:
            add_scorecard = date.date() == scorecard_date.date()

        if add_scorecard:
            return self.parse()

        return None
