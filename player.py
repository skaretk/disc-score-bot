
class Player:
    def __init__(self, name, total, score):
        self.name = name
        self.total = total
        self.score = score
        self.holes = []
        self.score_cards = 1

    def __str__(self):
        return f'{self.name} **{self.score}**'

    #def __lt__(self, other):
    #    return True if self.score < other.score else False
  
    #def __le__(self, other):
    #    return True if self.score <= other.score else False
  
    #def __ne__(self, other):
    #    return True if self.score != other.score else False
  
    #def __gt__(self, other):
    #    return True if self.score > other.score else False
  
    #def __ge__(self, other):
    #    return True if self.score >= other.score else False
    
    def __eq__(self, other):
        return True if self.name.lower().replace(" ", "") == other.name.lower().replace(" ", "") else False
    
    def __add__(self, other):
        player = Player(self.name, self.total + other.total, self.score + other.score)
        player.score_cards = self.score_cards + 1
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
    
    def get_first_name(self):
        return self.name.split(' ', 1)[0]

    def get_full_info(self):
     return f'{self} Kast: {self.total} - Scorecards: {self.score_cards}'
