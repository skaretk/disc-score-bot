
class Player:
    def __init__(self, name, total, score):
        self.name = name
        self.total = total
        self.score = score
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
        return True if self.name == other.name else False
    
    def __add__(self, other):
        player = Player(self.name, self.total + other.total, self.score + other.score)
        player.score_cards = self.score_cards + 1
        return player

    def get_full_info(self):
     return f'{self} Kast: {self.total} - Scorecards: {self.score_cards}'
