import datetime
import discord
from score.validate_embed import ValidateEmbed

class Scorecard:
    def __init__(self, coursename, layoutname, date_time, par):
        self.coursename = coursename
        self.course_url = ""
        self.layoutname = layoutname
        self.date_time = datetime.datetime.strptime(date_time,'%Y-%m-%d %H:%M')
        self.par = par
        self.players = []
        self.holes = {}

    def __str__(self):
        msg = f'{self.coursename} Dato: {self.date_time} Par: {self.par}'
        for player in self.players:
            msg += f'\n{player}'
        return msg

    def get_csv(self):
        header = []
        data = []
        date = self.date_time.strftime('%Y-%m-%d %H:%M')
        header = ['PlayerName', 'CourseName', 'LayoutName', 'Date', 'Total', '+/-']
        course_header = ['Par', self.coursename, self.layoutname, date, self.par, '']

        for hole in self.holes:
            header.append(f'Hole{hole}')
            course_header.append(self.holes[hole])
        data.append(course_header)

        for player in self.players:
            player_csv = [player.player_name, self.coursename, self.layoutname, date, player.total, player.score]
            for score in player.holes:
                player_csv.append(score)
            data.append(player_csv)
        return header, data

    def add_hole(self, no, par):
        self.holes[no] = par
    
    def get_players(self):
        players = ''
        for player in self.players:
            curr_player_str = f'{player.score_cards_position[0]} {player}'
            if player == self.players[0]:
                players += curr_player_str
            else:
                players += f'\n{curr_player_str}'
        return players

    def add_player(self, player):
        self.players.append(player)
        self.sort_players()
        self.add_player_position()
    
    def sort_players(self):
        self.players.sort(key=lambda x: x.score)
    
    def add_player_position(self):
        last_score = ""
        no = 0
        no_same_scores = 0
        for player in self.players:  
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
        embed = self.get_embed_max(thumbnail)
        validate_embed = ValidateEmbed(embed)
        if (validate_embed.validate() == True):
            return embed
        else:
            embed = self.get_embed_min(thumbnail)
            validate_embed = ValidateEmbed(embed)
            if (validate_embed.validate() == True):
                return embed
            else:
                return None

    def get_embed_min(self, thumbnail=''):
        embed=discord.Embed(title=self.coursename, url=self.course_url, description=f'{self.date_time}', color=0xFF5733)
        embed.add_field(name="Scores", value=f'{self.get_players()}', inline=False)
        if thumbnail != '':
            embed.set_thumbnail(url=(thumbnail))

        return embed
    
    def get_embed_max(self, thumbnail=''):
        embed=discord.Embed(title=self.coursename, url=self.course_url, description=f'{self.date_time} Par:{self.par}', color=0xFF5733)
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
