from .statistics import Statistics
from .point_system import PointSystem

class PlayerName:
    def __init__(self, name, alias = []):
        self.name = name
        self.alias = alias

    def __str__(self):
        return self.name
    
    def __len__(self):
        return len(self.name)

    def __eq__(self, other):
        if self.name.lower().replace(" ", "") == other.name.lower().replace(" ", ""):
            return True
        elif len(self.alias) != 0:
            if self.has_alias(other.name):
                return True
        return False

    def has_alias(self, name):
        search_name = name.lower().replace(" ", "")
        if type(self.alias) is list:
            if search_name in [alias.lower().replace(" ", "") for alias in self.alias]:
                print(f'{str(name)} has {len(self.alias)} aliases stored')
                return True
        else: # Not a list
            if (search_name == self.alias.lower().replace(" ", "")):
                print(f'{str(name)} has an alias stored')
                return True
        
        return False

class Player:
    def __init__(self, player_name, total, score):
        self.player_name = player_name
        self.total = int(total)
        self.score = int(score)
        self.holes = []
        self.score_cards = 1
        self.score_cards_position = []
        self.league_pts = 0
        self.league_attendence = 0
        self.player_stats = Statistics()

    def __str__(self):
        return f'{self.player_name} {self.score}'
    
    def __eq__(self, other):
        if self.player_name == other.player_name:
            return True
        else:
            return False
    
    def __add__(self, other):
        player = Player(PlayerName(self.player_name.name, self.player_name.alias), self.total + other.total, self.score + other.score)
        player.score_cards = self.score_cards + 1
        player.score_cards_position = self.score_cards_position + other.score_cards_position
        player.player_stats = self.player_stats + other.player_stats
        return player

    def add_hole(self, score):
        self.holes.append(score)
    
    def get_scores(self, from_hole = '', to_hole = ''):
            scores = ''
            if from_hole and to_hole:
                current_hole = from_hole-1
                for score in self.holes[from_hole-1:to_hole]:
                    if current_hole < 9:
                        scores += f'{score} '
                    else:
                        scores += f'{score}  '
                    current_hole += 1

            return scores

    def get_average_result(self):
        return sum(self.score_cards_position) / len(self.score_cards_position)
    
    def get_first_name(self):
        return self.player_name.name.split(' ', 1)[0]
    
    def calculate_attendence(self, no_scorecards):
         percentage = (self.score_cards / no_scorecards)*100
         self.league_attendence = percentage.__round__(2)

    def get_full_info(self):
     return f'{self} Kast: {self.total} - Kort: {self.score_cards}'

    def get_full_info_min(self):
        return f'{self}: {self.total}: {self.score_cards}'

    def get_league_info(self, scorecards):
        if (self.league_pts == 0):
            self.league_pts = PointSystem.calculate_scores(self.score_cards_position)
            self.calculate_attendence(scorecards)
        return f'{self}: Kast: {self.total}: Kort: {self.score_cards} ({self.league_attendence}%) Pts: {self.league_pts}'
           
