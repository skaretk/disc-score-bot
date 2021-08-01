
class Scorecard:
    def __init__(self, coursename, date, total):
        self.coursename = coursename
        self.date = date
        self.total = total
        self.playerlist = []

    def __str__(self):
        msg = f'{self.coursename} Dato: {self.date} Par: {self.total}'
        for player in self.playerlist:
            msg += f'\n{player}'
        return msg

    def add_player(self, player):
        self.playerlist.append(player)

    def print(self):
        print(self)
    
    def sort_players_score(self):
        self.playerlist.sort(key=lambda x: x.score)
    
    def sort_players_total(self):
        self.playerlist.sort(key=lambda x: x.total)

    def print_players(self):        
        for player in self.playerlist:
            print(player)