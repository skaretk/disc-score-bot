from .statistics import Statistics

class PlayerName:
    """Player Name class, contain players name and aliases"""
    def __init__(self, name, alias=None):
        self.name = name
        self.alias = alias

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.name)

    def __eq__(self, other):
        if self.name.lower().replace(" ", "") == other.name.lower().replace(" ", ""):
            return True
        if self.alias is not None:
            if self.has_alias(other.name):
                return True
        elif other.alias is not None:
            if other.has_alias(self.name):
                return True
        return False

    def has_alias(self, name):
        """Check if the players has any aliases"""
        search_name = name.lower().replace(" ", "")
        if self.alias is not None:
            if isinstance(self.alias, list):
                if search_name in [alias.lower().replace(" ", "") for alias in self.alias]:
                    return True
            else: # Not a list
                if search_name == self.alias.lower().replace(" ", ""):
                    return True

        return False

class Player:
    """Player Class"""
    def __init__(self, player_name, total, score):
        self.player_name = player_name
        self.total = int(total)
        self._score = int(score)
        self.holes = []
        self.division = ""
        self.payout = ""
        self.score_cards = 1
        self.score_cards_position = []
        self.league_pts = 0
        self.league_attendence = 0
        self.player_stats = Statistics()

    def __str__(self):
        return f'{self.player_name} {self.get_score()}'

    def __eq__(self, other):
        if self.player_name == other.player_name:
            return True
        else:
            return False

    def __add__(self, other):
        player = Player(PlayerName(self.player_name.name, self.player_name.alias), self.total + other.total, self._score + other._score)
        player.score_cards = self.score_cards + 1
        player.score_cards_position = self.score_cards_position + other.score_cards_position
        player.player_stats = self.player_stats + other.player_stats
        return player

    @property
    def score(self):
        """The players score"""
        return self._score

    @score.setter
    def score(self, score:int):
        self._score = score

    def get_score(self):
        """Get the score string, append + or set to E if par"""
        if self._score == 0:
            return 'E'
        if self._score > 0:
            return f'+{self._score}'
        return str(self._score)

    def add_hole(self, score):
        """Add a hole to the player"""
        self.holes.append(score)

    def get_scores(self, from_hole='', to_hole=''):
        """Get the scores from the player within the given holes"""
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
        """Get the average result of scorecard positions"""
        return sum(self.score_cards_position) / len(self.score_cards_position)

    def get_first_name(self):
        """Get the players first name"""
        return self.player_name.name.split(' ', 1)[0]

    def calculate_attendence(self, no_scorecards):
        """Calculate the attendence over the players scorecards"""
        percentage = (self.score_cards / no_scorecards)*100
        self.league_attendence = round(percentage, 2)

    def get_full_info(self):
        """Get the full info from the player"""
        return f'{self} Kast: {self.total} - Kort: {self.score_cards}'

    def get_full_info_min(self):
        """Get full info from the player, excluding extra info"""
        return f'{self}: {self.total}: {self.score_cards}'

    def get_league_info(self):
        """Get the league info from the player"""
        return f'{self}: Kast: {self.total}: Kort: {self.score_cards} ({self.league_attendence}%) Pts: {self.league_pts}'
