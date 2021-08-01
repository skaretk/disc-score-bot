
class Player:
    def __init__(self, name, total, score):
        self.name = name
        self.total = total
        self.score = score

    def __str__(self):
     return f'Spiller: {self.name} Score: {self.score} Kast: {self.total}'

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
        return Player(self.name, self.total + other.total, self.score + other.score)
