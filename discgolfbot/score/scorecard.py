import datetime
import nextcord
from discord_utils.embed_validation import validate_embed
from enum import Enum
from .course import Course
from .player import Player

class ScorecardTypes(Enum):
    UNKNOWN = 0
    UDISC_SCORECARD = 1
    UDISC_COMPETITION = 2

class Scorecard:
    def __init__(self):
        self._course = Course("")
        self._date_time = None
        self._par = None
        self._card_type = None
        self.divisions = []
        self.players = []
        self.holes = {}

    @property
    def course(self):
        return self._course

    @property
    def date_time(self):
        return self._date_time

    @date_time.setter
    def date_time(self, date_time):
        self._date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d %H:%M')

    @property
    def par(self):
        return self._par

    @par.setter
    def par(self, par):
        self._par = par

    @property
    def card_type(self):
        return self._card_type

    @card_type.setter
    def card_type(self, type):
        self._card_type = type

    def __str__(self):
        msg = f'{self.course.name} Dato: {self.date_time} Par: {self.par}'
        for player in self.players:
            msg += f'\n{player}'
        return msg

    def get_csv(self):
        header = []
        data = []
        date = self.date_time.strftime('%Y-%m-%d %H:%M')
        header = ['PlayerName', 'CourseName', 'LayoutName', 'Date', 'Total', '+/-']
        course_header = ['Par', self.course.name, self.course.layout, date, self.par, '']

        for hole in self.holes:
            header.append(f'Hole{hole}')
            course_header.append(self.holes[hole])
        data.append(course_header)

        for player in self.players:
            player_csv = [player.player_name, self.course.name, self.course.layout, date, player.total, player.score]
            for score in player.holes:
                player_csv.append(score)
            data.append(player_csv)
        return header, data

    def add_hole(self, no, par):
        self.holes[no] = par

    def get_players(self, division=""):
        players = ''
        for player in self.players:
            if player.division == division:
                curr_player_str = f'{player.score_cards_position[0]} {player}'
                if player == self.players[0]:
                    players += curr_player_str
                else:
                    players += f'\n{curr_player_str}'
        return players

    def add_player(self, player: Player):
        self.players.append(player)
        if player.division not in self.divisions:
            self.divisions.append(player.division)
        self.sort_players()
        self.add_player_position()

    def sort_players(self):
        self.players.sort(key=lambda x: x.score)

    def add_player_position(self):
        for division in self.divisions:
            last_score = ""
            no = 0
            no_same_scores = 0
            for player in self.players:
                if player.division == division:
                    if last_score == player.score:
                        no_same_scores += 1
                    else:
                        no += no_same_scores + 1
                        no_same_scores = 0

                    player.score_cards_position.clear()
                    player.score_cards_position.append(no)
                    last_score = player.score

    def get_total_throws(self):
        throws = 0
        for player in self.players:
            throws += player.total
        return throws

    def get_max_length_player_name(self, only_first_name = False):
        max_length = 0
        for player in self.players:
            if only_first_name:
                first_name = player.get_first_name()
                if len(first_name) > max_length:
                    max_length = len(first_name)
            else:
                if len(player.player_name) > max_length:
                    max_length = len(player.player_name)
        return max_length

    def get_embed_column_start(self, str, only_first_name = False):
        offset = self.get_max_length_player_name(only_first_name) - len(str)
        str += ' ' * offset + ' '
        return str

    def get_embed_pars_row(self, from_hole = '', to_hole = ''):
            pars = ''
            for hole in self.holes:
                if (hole < from_hole):
                    continue
                elif (hole > to_hole):
                    break
                if (hole <= 9):
                    pars += f'{self.holes[hole]} '
                else:
                    pars += f'{self.holes[hole]}  '
            return pars

    def get_embed_holes_row(self, from_hole = '', to_hole = ''):
            holes = ''
            if from_hole and to_hole:
                current_hole = from_hole
                for hole in range(from_hole, to_hole+1):
                    holes += f'{hole} '
                    current_hole += 1

            return holes

    def get_embed(self, thumbnail=''):
        embed = self.get_embed_min(thumbnail)
        if (validate_embed(embed) == True):
            return embed
        else:
            return None

    def get_embed_min(self, thumbnail=''):
        embed=nextcord.Embed(title=self.course.name, url=self.course.url, description=f'{self.date_time}', color=0x004899)
        for division in self.divisions:
            embed.add_field(name=f'{division}', value=f'```{self.get_players(division)}```', inline=False)
        if thumbnail != '':
            embed.set_thumbnail(url=(thumbnail))

        return embed

    def get_embed_max(self, thumbnail=''):
        embed=nextcord.Embed(title=self.course.name, url=self.course.url, description=f'{self.date_time} Par:{self.par}', color=0x004899)
        embed.add_field(name="Scores", value=f'{self.get_players()}', inline=False)

        header_holes = self.get_embed_column_start('Hole', True)
        header_par = self.get_embed_column_start('Par', True)

        no_of_holes = len(self.holes)
        if no_of_holes <= 12:
            holes = self.get_embed_holes_row(1, no_of_holes)
            pars = self.get_embed_pars_row(1, no_of_holes)
            scores = ''
            for player in self.players:
                player_str = self.get_embed_column_start(player.get_first_name(), True)
                scores += f'{player_str}{player.get_scores(1,no_of_holes)}\n'

            embed.add_field(name=f'Holes 1-{no_of_holes}', value=f'```{header_holes}{holes}\n{header_par}{pars}\n{scores}```', inline=False)
        elif no_of_holes <= 18:
            holes_1 = self.get_embed_holes_row(1, 9)
            holes_2 = self.get_embed_holes_row(10, no_of_holes)
            pars_1 = self.get_embed_pars_row(1, 9)
            pars_2 = self.get_embed_pars_row(10, no_of_holes)

            scores_1 = ''
            scores_2 = ''
            for player in self.players:
                player_str = self.get_embed_column_start(player.get_first_name(), True)
                scores_1 += f'{player_str}{player.get_scores(1,9)}\n'
                scores_2 += f'{player_str}{player.get_scores(10, no_of_holes)}\n'

            embed.add_field(name=f'Holes 1-9', value=f'```{header_holes}{holes_1}\n{header_par}{pars_1}\n{scores_1}```', inline=False)
            embed.add_field(name=f'Holes 10-{no_of_holes}', value=f'```{header_holes}{holes_2}\n{header_par}{pars_2}\n{scores_2}```', inline=False)

        elif no_of_holes <= 27:
            pars_1 = self.get_embed_pars_row(1, 9)
            pars_2 = self.get_embed_pars_row(10, 18)
            pars_3 = self.get_embed_pars_row(19, no_of_holes)
            holes_1 = self.get_embed_holes_row(1, 9)
            holes_2 = self.get_embed_holes_row(10, 18)
            holes_3 = self.get_embed_holes_row(19, no_of_holes)

            scores_1 = ''
            scores_2 = ''
            scores_3 = ''
            for player in self.players:
                player_str = self.get_embed_column_start(player.get_first_name(), True)
                scores_1 += f'{player_str}{player.get_scores(1,9)}\n'
                scores_2 += f'{player_str}{player.get_scores(10, 18)}\n'
                scores_3 += f'{player_str}{player.get_scores(19, no_of_holes)}\n'

            embed.add_field(name=f'Holes 1-9', value=f'```{header_holes}{holes_1}\n{header_par}{pars_1}\n{scores_1}```', inline=False)
            embed.add_field(name=f'Holes 10-18', value=f'```{header_holes}{holes_2}\n{header_par}{pars_2}\n{scores_2}```', inline=False)
            embed.add_field(name=f'Holes 19-{no_of_holes}', value=f'```{header_holes}{holes_3}\n{header_par}{pars_3}\n{scores_3}```', inline=False)

        if thumbnail != '':
            embed.set_thumbnail(url=(thumbnail))

        return embed
