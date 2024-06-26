import dateutil.parser as dparser
import nextcord
from discord_utils.embed_validation import validate_embed
from .player import Player
from .udisc.udisc_player import UdiscPlayer
from .course import Course

class Scorecard:
    """Scorecard class"""
    def __init__(self):
        self._course = Course()
        self._date_time = None
        self._par = None
        self.divisions = []
        self.players = []
        self.holes = {}

    def __str__(self):
        return f'{self.date_time} - {self.course.name} Par: {self.par}'

    @property
    def course(self):
        """Scorecard course"""
        return self._course

    @property
    def date_time(self):
        """Scorecard date"""
        return self._date_time

    @date_time.setter
    def date_time(self, date_time):
        try:
            self._date_time = dparser.parse(date_time, fuzzy=True)
        except dparser.ParserError:
            self._date_time = None

    @property
    def par(self):
        """scorecard par"""
        return self._par

    @par.setter
    def par(self, par):
        self._par = par

    def get_csv(self):
        """Get the csv file, must be overrided in child classes"""

    def add_hole(self, number, par):
        """Add a hole to the scorecard"""
        self.holes[number] = par

    def get_players_str(self):
        """Return a string containing all players and their division/scores"""
        players_str = ''
        for division in self.divisions:
            players_str += f'\n{division}\n{self.get_players(division)}'
        return players_str

    def get_players(self, division=""):
        """Get all players in the given division"""
        players = ''
        first_player = True
        for player in self.players:
            if player.division == division:
                curr_player_str = f'{player.score_cards_position[0]} {self.add_column_offset(str(player.name))} {player.get_score()}'
                if player.rating is not None:
                    if isinstance(player, UdiscPlayer):
                        curr_player_str = f'{curr_player_str} [{str(player.get_pdga_rating())}]'
                    else:
                        curr_player_str = f'{curr_player_str} [{str(player.rating)}]'
                if first_player is True:
                    players += curr_player_str
                    first_player = False
                else:
                    players += f'\n{curr_player_str}'
        return players

    def add_player(self, player:Player):
        """Add a Player to the scorecard, sort and add the position"""
        self.players.append(player)
        if player.division not in self.divisions:
            self.divisions.append(player.division)
        self.sort_players()
        self.add_player_position()

    def sort_players(self):
        """Sort players based on the score"""
        self.players.sort(key=lambda p: p.score)

    def add_player_position(self):
        """Add the player position in all of the divisions"""
        for division in self.divisions:
            last_score = ""
            position = 0
            no_same_scores = 0
            for player in self.players:
                if player.division == division:
                    if last_score == player.score:
                        no_same_scores += 1
                    else:
                        position += no_same_scores + 1
                        no_same_scores = 0

                    player.score_cards_position.clear()
                    player.score_cards_position.append(position)
                    last_score = player.score

    def get_total_throws(self):
        """Returns total throws in the scorecard"""
        throws = 0
        for player in self.players:
            throws += player.total
        return throws

    def get_longest_player_name(self, only_first_name=False):
        """Returns the lenth of the longest player name"""
        max_length = 0
        for player in self.players:
            if only_first_name:
                first_name = player.get_first_name()
                if len(first_name) > max_length:
                    max_length = len(first_name)
            else:
                if len(str(player.name)) > max_length:
                    max_length = len(str(player.name))
        return max_length

    def add_column_offset(self, string, only_first_name=False):
        """Adds a column offset to the given string, for easier show the scores"""
        offset = self.get_longest_player_name(only_first_name) - len(string)
        string += ' ' * offset + ' '
        return string

    def get_pars_str(self, from_hole='', to_hole=''):
        """Return the pars from the given holes"""
        pars = ''
        for hole_number, hole in self.holes.items():
            if hole_number < from_hole:
                continue
            if hole_number > to_hole:
                break
            if hole_number <= 9:
                pars += f'{hole} '
            else:
                pars += f'{hole}  '
        return pars

    def get_holes_str(self, from_hole='', to_hole=''):
        """Return the holes between given holes"""
        holes = ''
        if from_hole and to_hole:
            current_hole = from_hole
            for hole in range(from_hole, to_hole+1):
                holes += f'{hole} '
                current_hole += 1

        return holes

    def append_field(self, embed=nextcord.Embed):
        """Append a field to the given embed, must be overrided in the child classes"""

    def get_embed(self, thumbnail=''):
        """Get the nextcord.Embed"""
        embed = self.get_small_embed(thumbnail)
        if validate_embed(embed):
            return embed
        return None

    def get_small_embed(self, thumbnail=''):
        """Get a small embed, only containing scores"""
        embed_title = self.course.name if self.course.name is not None else ''
        embed=nextcord.Embed(title=embed_title, url=self.course.url, description=f'{self.date_time}', color=0x004899)
        for division in self.divisions:
            embed.add_field(name=f'{division}', value=f'```{self.get_players(division)}```', inline=False)
        if thumbnail != '':
            embed.set_thumbnail(url=thumbnail)

        return embed

    def get_big_embed(self, thumbnail=''):
        """Get a big embed, including scores for each hole"""
        embed_title = self.course.name if self.course.name is not None else ''
        embed=nextcord.Embed(title=embed_title, url=self.course.url, description=f'{self.date_time} Par:{self.par}', color=0x004899)
        embed.add_field(name="", value=f'```{self.get_players()}```', inline=False)

        header_holes = self.add_column_offset('Hole', True)
        header_par = self.add_column_offset('Par', True)

        no_of_holes = len(self.holes)
        if no_of_holes <= 12:
            holes = self.get_holes_str(1, no_of_holes)
            pars = self.get_pars_str(1, no_of_holes)
            scores = ''
            for player in self.players:
                player_str = self.add_column_offset(player.get_first_name(), True)
                scores += f'{player_str}{player.get_scores(1,no_of_holes)}\n'

            embed.add_field(name=f'Holes 1-{no_of_holes}', value=f'```{header_holes}{holes}\n{header_par}{pars}\n{scores}```', inline=False)
        elif no_of_holes <= 18:
            holes_1 = self.get_holes_str(1, 9)
            holes_2 = self.get_holes_str(10, no_of_holes)
            pars_1 = self.get_pars_str(1, 9)
            pars_2 = self.get_pars_str(10, no_of_holes)

            scores_1 = ''
            scores_2 = ''
            for player in self.players:
                player_str = self.add_column_offset(player.get_first_name(), True)
                scores_1 += f'{player_str}{player.get_scores(1,9)}\n'
                scores_2 += f'{player_str}{player.get_scores(10, no_of_holes)}\n'

            embed.add_field(name='Holes 1-9', value=f'```{header_holes}{holes_1}\n{header_par}{pars_1}\n{scores_1}```', inline=False)
            embed.add_field(name=f'Holes 10-{no_of_holes}', value=f'```{header_holes}{holes_2}\n{header_par}{pars_2}\n{scores_2}```', inline=False)

        elif no_of_holes <= 27:
            pars_1 = self.get_pars_str(1, 9)
            pars_2 = self.get_pars_str(10, 18)
            pars_3 = self.get_pars_str(19, no_of_holes)
            holes_1 = self.get_holes_str(1, 9)
            holes_2 = self.get_holes_str(10, 18)
            holes_3 = self.get_holes_str(19, no_of_holes)

            scores_1 = ''
            scores_2 = ''
            scores_3 = ''
            for player in self.players:
                player_str = self.add_column_offset(player.get_first_name(), True)
                scores_1 += f'{player_str}{player.get_scores(1,9)}\n'
                scores_2 += f'{player_str}{player.get_scores(10, 18)}\n'
                scores_3 += f'{player_str}{player.get_scores(19, no_of_holes)}\n'

            embed.add_field(name='Holes 1-9', value=f'```{header_holes}{holes_1}\n{header_par}{pars_1}\n{scores_1}```', inline=False)
            embed.add_field(name='Holes 10-18', value=f'```{header_holes}{holes_2}\n{header_par}{pars_2}\n{scores_2}```', inline=False)
            embed.add_field(name=f'Holes 19-{no_of_holes}', value=f'```{header_holes}{holes_3}\n{header_par}{pars_3}\n{scores_3}```', inline=False)

        if thumbnail != '':
            embed.set_thumbnail(url=thumbnail)

        return embed
