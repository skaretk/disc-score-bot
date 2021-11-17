import discord
from discord_utils.embed_validation import validate_embed
from score.statistics import Statistics

class Scorecards:
    def __init__(self):
        self.scorecards = []
        self.players = []
        self.statistics = Statistics()
    
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
            
            msg += f'\n{no}: {player.get_full_info()}'

            last_score = player.score
            
        return msg
    
    def add_scorecard(self, scorecard, alias):        
        for player in scorecard.players:
            player_alias = alias.get_player_alias(player.player_name.name)
            if player_alias != None:
                idx = scorecard.players.index(player)
                scorecard.players[idx].player_name.alias = player_alias
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
    
    def sort_players_points(self):
        self.players.sort(key=lambda x: x.league_pts, reverse=True)
    
    def get_league_str(self):
        msg = ''
        no = 0
        last_pts = ''
        no_same_pts = 0
        for player in self.players:  
            if last_pts == player.league_pts:
                no_same_pts += 1
            else:
                no += no_same_pts + 1
                no_same_pts = 0
            
            msg += f'\n{no}: {player.get_league_info(len(self.scorecards))}'

            last_pts = player.league_pts
            
        return msg
    
    def sort_players_position(self):
        self.players.sort(key=lambda x: x.get_average_result())

    def get_total_throws(self):
        throws = 0
        for scorecard in self.scorecards:
            throws += scorecard.get_total_throws()
        return throws

    def get_total_stats(self):
        for player in self.players:
            self.statistics += player.player_stats

    def print_scores(self):
        print("Total Scores")
        for player in self.players:
            print(player)
    
    # Check and return the biggeest embed, return None if not possible
    def get_embed(self, thumbnail=''):        
        embed = self.get_embed_max(thumbnail)
        if (validate_embed(embed) == True):
            return embed
        else:
            embed = self.get_embed_min(thumbnail)
            if (validate_embed(embed) == True):
                return embed
            else:
                return None

    def get_embed_league(self, thumbnail=''):
        embed=discord.Embed(title="EDK League", url="", description="", color=0x004899)
        embed.set_footer(text=f'Total{self.get_league_str()}')
        if thumbnail != '':
            embed.set_thumbnail(url=(thumbnail))
        
        if (validate_embed(embed) == True):
            return embed
        else:
            return None
    
    def get_embed_max(self, thumbnail=''):
        embed=discord.Embed(title="Scores", url="", description="", color=0x004899)
        for scorecard in self.scorecards:
            embed.add_field(name=scorecard.coursename, value=f'{scorecard.date_time.date()} Par:{scorecard.par}\n{scorecard.get_players()}', inline=False)
            if (len(self.scorecards) > 1):
                embed.set_footer(text=f'Total{self}')
        if thumbnail != '':
            embed.set_thumbnail(url=(thumbnail))

        return embed
    
    def get_embed_min(self, thumbnail=''):
        embed=discord.Embed(title="Total", url="", description=f'{self}', color=0x004899)        
        score_cards = ''
        for scorecard in self.scorecards:
            score_cards += f'{scorecard.date_time.date()} - {scorecard.coursename}\n'
        embed.add_field(name="Kort", value=f'{score_cards}')            
        if thumbnail != '':
            embed.set_thumbnail(url=(thumbnail))

        return embed
    
    def get_embed_stats(self, thumbnail=''):        
        embed=discord.Embed(title="Stats", url="", description="Statistics for saved scorecards", color=0x004899)
        embed.add_field(name="Scorecards", value=f'{len(self.scorecards)}', inline=False)
        embed.add_field(name="Players", value=f'{len(self.players)}', inline=False)
        self.get_total_stats()
        embed.add_field(name="Throws", value=f'{self.get_total_throws()}', inline=False)
        embed.add_field(name="Aces", value=f'{self.statistics.ace}', inline=False )
        embed.add_field(name="Eagles", value=f'{self.statistics.eagle}', inline=False )
        embed.add_field(name="Birdies", value=f'{self.statistics.birdie}', inline=False )
        embed.add_field(name="Pars", value=f'{self.statistics.par}', inline=False )
        embed.add_field(name="Bogey", value=f'{self.statistics.bogey}', inline=False )
        embed.add_field(name="Double Bogey", value=f'{self.statistics.double_bogey}', inline=False )
        embed.add_field(name="Triple Bogey+", value=f'{self.statistics.triple_bogey_plus}', inline=False )
        

        if thumbnail != '':
            embed.set_thumbnail(url=(thumbnail))

        return embed
    
    def save_scorecards_text(self, file):
        str = f'{self.get_league_str()}\n'
        for scorecard in self.scorecards:
            str += f'\n{scorecard.date_time.date()} - {scorecard.coursename}'
        f = open(file, "a")
        f.write(str)
        f.close()
