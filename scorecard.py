import datetime

class Scorecard:
    def __init__(self, coursename, date_time, par):
        self.coursename = coursename
        self.date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d %H:%M' )
        self.par = par
        self.playerlist = []

    def __str__(self):
        msg = f'{self.coursename} Dato: {self.date_time} Par: {self.par}'
        for player in self.playerlist:
            msg += f'\n{player}'
        return msg
    
    def get_players(self):
        players = ''
        for player in self.playerlist:
            players += f'\n{player}'
        return players

    def add_player(self, player):
        self.playerlist.append(player)
    
    def sort_players(self):
        self.playerlist.sort(key=lambda x: x.score)

    def print_players(self):        
        for player in self.playerlist:
            print(player)