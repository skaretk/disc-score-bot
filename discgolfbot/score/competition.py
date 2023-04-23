from datetime import datetime
import nextcord
from pathlib import Path
from discord_utils.embed_validation import validate_embed
from .statistics import Statistics
from .alias import Alias
from .files.udisccsvreader import UdiscCsvReader

class Competition:
    """Competition Class - Collection of scorecards"""
    def __init__(self):
        self.scorecards = []
        self.players = []
        self.statistics = Statistics()

    def __str__(self):
        msg = ''
        position = 0
        last_score = ''
        no_same_scores = 0
        for player in self.players:
            if last_score == player.score:
                no_same_scores += 1
            else:
                position += no_same_scores + 1
                no_same_scores = 0

            msg += f'\n{position}: {player.get_full_info()}'
            last_score = player.score

        return msg

    def add_scorecard(self, scorecard):
        """Add Scorecard and its players"""
        self.scorecards.append(scorecard)
        self.add_players(scorecard)

    def add_player(self, new_player):
        """Add a new player"""
        self.players.append(new_player)
        self.sort_players()

    def add_players(self, scorecard):
        """Add all players from a scorecard"""
        for player in scorecard.players:
            if self.player_exist(player):
                idx = self.players.index(player)
                self.players[idx] += player
            else:
                self.add_player(player)

    def add_player_alias(self, player, alias:Alias):
        """Add alias to given player"""
        player_with_alias = alias.get_player_with_alias(str(player.name))
        if player_with_alias is not None:
            player.name = player_with_alias

    def player_exist(self, player):
        """Check if player exists"""
        if player in self.players:
            return True
        return False

    def sort_players(self):
        """Sort players by score"""
        self.players.sort(key=lambda x: x.score)

    def sort_players_points(self):
        """Sort players by league points"""
        self.players.sort(key=lambda x: x.league_pts, reverse=True)

    def sort_players_position(self):
        """Sort Players by average result"""
        self.players.sort(key=lambda x: x.get_average_result())

    def get_total_throws(self):
        """Get total throws"""
        throws = 0
        for scorecard in self.scorecards:
            throws += scorecard.get_total_throws()
        return throws

    def calculate_statistics(self):
        """Calculate the statistics"""
        for player in self.players:
            self.statistics += player.player_stats

    def get_embed(self, thumbnail=''):
        """Check and return the biggest embed, return None if not possible"""
        embed = self.get_big_embed(thumbnail)
        if validate_embed(embed):
            return embed

        embed = self.get_small_embed(thumbnail)
        if validate_embed(embed):
            return embed

        return None

    def get_big_embed(self, thumbnail=''):
        """Get the largest embed, including scores"""
        embed=nextcord.Embed(title="Scores", url="", description="", color=0x004899)
        for scorecard in self.scorecards:
            scorecard.append_field(embed)

        if len(self.scorecards) > 1:
            embed.set_footer(text=f'Total{self}')
        if thumbnail != '':
            embed.set_thumbnail(url=thumbnail)

        return embed

    def get_small_embed(self, thumbnail=''):
        """Get small embed, only scorecards and total score"""
        embed=nextcord.Embed(title="Scores", url="", description="", color=0x004899)
        score_cards = ''
        for scorecard in self.scorecards:
            score_cards += f'{str(scorecard)}\n'
        embed.add_field(name="Scorecards", value=f'{score_cards}')
        embed.set_footer(text=f'Total{self}')
        if thumbnail != '':
            embed.set_thumbnail(url=thumbnail)

        return embed

    def get_stats_embed(self, thumbnail=''):
        """Get statistics as embed"""
        embed=nextcord.Embed(title="Stats", url="", description="Statistics for scorecards", color=0x004899)
        embed.add_field(name="Scorecards", value=f'{len(self.scorecards)}', inline=False)
        embed.add_field(name="Players", value=f'{len(self.players)}', inline=False)
        self.calculate_statistics()
        embed.add_field(name="Throws", value=f'{self.get_total_throws()}', inline=False)
        embed.add_field(name="Aces", value=f'{self.statistics.ace}', inline=False )
        embed.add_field(name="Eagles", value=f'{self.statistics.eagle}', inline=False )
        embed.add_field(name="Birdies", value=f'{self.statistics.birdie}', inline=False )
        embed.add_field(name="Pars", value=f'{self.statistics.par}', inline=False )
        embed.add_field(name="Bogeys", value=f'{self.statistics.bogey}', inline=False )
        embed.add_field(name="Double Bogeys", value=f'{self.statistics.double_bogey}', inline=False )
        embed.add_field(name="Triple Bogeys+", value=f'{self.statistics.triple_bogey_plus}', inline=False )

        if thumbnail != '':
            embed.set_thumbnail(url=thumbnail)

        return embed

    def save_scorecards_text(self, file):
        """Save the scorecards as a text file"""
        txt = f'{self}\n'
        for scorecard in self.scorecards:
            txt += f'\n{str(scorecard)}'
        file_to_write = open(file, "a", encoding="utf-8")
        file_to_write.write(txt)
        file_to_write.close()

    @staticmethod
    def parse(path:Path, alias:Alias):
        """Get all scorecards"""
        competition = Competition()
        for file in list(path.iterdir()):
            if file.suffix == ".csv":
                reader = UdiscCsvReader(file)
                scorecard = reader.parse()

                # Add aliases
                for player in scorecard.players:
                    competition.add_player_alias(player, alias)

                competition.add_scorecard(scorecard)

        return competition

    @staticmethod
    def parse_course(path:Path, alias:Alias, course):
        """Get all scorecards for a course"""
        competition = Competition()
        for file in list(path.iterdir()):
            if file.suffix == ".csv":
                reader = UdiscCsvReader(file)
                scorecard = reader.contain_course(course)

                if scorecard is not None and scorecard.course.name is not None:
                    if course.lower() in scorecard.course.name.lower():
                        # Add aliases
                        for player in scorecard.players:
                            competition.add_player_alias(player, alias)

                        competition.add_scorecard(scorecard)

        return competition

    @staticmethod
    def parse_dates(path:Path, alias:Alias, date:datetime, date_to:datetime):
        """Get all scorecards within date(s)"""
        competition = Competition()
        for file in list(path.iterdir()):
            if file.suffix == ".csv":
                reader = UdiscCsvReader(file)
                scorecard = reader.contain_dates(date, date_to)

                if scorecard is not None:
                    # Add aliases
                    for player in scorecard.players:
                        competition.add_player_alias(player, alias)

                    competition.add_scorecard(scorecard)

        return competition
