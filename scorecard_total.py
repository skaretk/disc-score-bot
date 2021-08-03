class Scorecard_total:
    def __init__(self):
        self.scorecardlist = []
        self.playerlist = []
    
    def __str__(self):
        msg = ''
        no = 1
        for player in self.playerlist:
            msg += f'\n{no}: {player.get_full_info()}'
            no += 1
        return msg
    
    def add_scorecard(self, scorecard):
        self.scorecardlist.append(scorecard)
    
    def add_player(self, new_player):
        self.playerlist.append(new_player)
    
    def player_exist(self, new_player):
        if (new_player in self.playerlist):
            return True
        else:
            return False
    
    def sort_players(self):
        self.playerlist.sort(key=lambda x: x.score)

    def print_scores(self):
        print("Total Scores")
        for player in self.playerlist:
            print(player)