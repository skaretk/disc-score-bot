import discord

class Scorecards:
    def __init__(self):
        self.scorecards = []
        self.players = []
    
    def __str__(self):
        msg = ''
        no = 0
        last_score = ''
        no_same_scores = 0
        for player in self.players:  
            if last_score == player.score:
                no_same_scores += 1
            else:
                no += no_same_scores + 1
                no_same_scores = 0
            
            msg += f'\n> {no}: {player.get_full_info()}'

            last_score = player.score
            
        return msg
    
    def add_scorecard(self, scorecard, alias):        
        for player in scorecard.players:
            player_alias = alias.get_player_alias(player.name)
            if player_alias != None:
                idx = scorecard.players.index(player)
                scorecard.players[idx].add_alias(player_alias)
        self.scorecards.append(scorecard)
        self.add_players(scorecard)        
    
    def add_player(self, new_player):
        self.players.append(new_player)
        self.sort_players()
    
    def add_players(self, scorecard):
        for player in scorecard.players:
            if self.player_exist(player):
                idx = self.players.index(player)
                self.players[idx] += player
            else:
                self.add_player(player)
    
    def player_exist(self, new_player):
        if (new_player in self.players):
            return True
        else:
            return False
    
    def sort_players(self):
        self.players.sort(key=lambda x: x.score)

    def print_scores(self):
        print("Total Scores")
        for player in self.players:
            print(player)
    
    def get_embed(self, thumbnail=''):
        embed=discord.Embed(title="Disc Score Bot", url="", description="", color=0xFF5733)
        for scorecard in self.scorecards:
            embed.add_field(name=scorecard.coursename, value=f'{scorecard.date_time.date()} Par:{scorecard.par}\n{scorecard.get_players()}', inline=True)    
        embed.add_field(name="Total", value=self, inline=False)
        if thumbnail != '':
            embed.set_thumbnail(url=(thumbnail))

        return embed