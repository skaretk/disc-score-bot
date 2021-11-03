
class PlayerName:
    def __init__(self, name, alias = ''):
        self.name = name
        self.alias = alias

    def __str__(self):
        return self.name
    
    def __len__(self):
        return len(self.name)

    def __eq__(self, other):
        if self.name.lower().replace(" ", "") == other.name.lower().replace(" ", ""):
            return True
        elif self.alias.lower().replace(" ", "") == other.name.lower().replace(" ", ""):
            return True
        else:
            return False

class Player:
    def __init__(self, player_name, total, score):
        self.player_name = player_name
        self.total = int(total)
        self.score = int(score)
        self.holes = []
        self.score_cards = 1
        self.score_cards_position = []

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

    def get_full_info(self):
     return f'{self} Kast: {self.total} - Kort: {self.score_cards}'

    def get_full_info_min(self):
        return f'{self}: {self.total}: {self.score_cards}'
