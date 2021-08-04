import discord

class Scorecard_total:
    def __init__(self):
        self.scorecardlist = []
        self.playerlist = []
    
    def __str__(self):
        msg = ''
        no = 0
        last_score = ''
        no_same_scores = 0
        for player in self.playerlist:  
            if last_score == player.score:
                no_same_scores += 1
            else:
                no += no_same_scores + 1
                no_same_scores = 0
            
            msg += f'\n{no}: {player.get_full_info()}'

            last_score = player.score
            
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
    
    def get_embed(self, thumbnail=''):
        embed=discord.Embed(title="Disc Score Bot", url="", description="", color=0xFF5733)
        for scorecard in self.scorecardlist:
            embed.add_field(name=scorecard.coursename, value=f'{scorecard.date_time.date()} Par:{scorecard.par}\n{scorecard.get_players()}', inline=True)    
        embed.add_field(name="Total", value=self, inline=False)
        if thumbnail != '':
            embed.set_thumbnail(url=(thumbnail))

        return embed