import nextcord
from discord_utils.embed_validation import validate_embed
from score.scorecard import Scorecard
from .udisc import LOGO_URL

class UdiscScoreCardOld(Scorecard):
    """old uDisc Scorecard"""

    def __str__(self):
        return f'{self.date_time} - {self.course.name}: {self.course.layout}'

    def append_field(self, embed=nextcord.Embed):
        embed.add_field(name=f'{self.course.name} ({self.course.layout}) {self.date_time.date()}', value=f'```{self.get_players()}```', inline=False)

    def get_csv(self):
        header = ['PlayerName', 'CourseName', 'LayoutName', 'Date', 'Total', '+/-']
        data = []
        date = self.date_time.strftime('%Y-%m-%d %H:%M')
        course_header = ['Par', self.course.name, self.course.layout, date, self.par, '']

        for hole in self.holes.items():
            header.append(f'Hole{hole}')
            course_header.append(hole)
        data.append(course_header)

        for player in self.players:
            player_csv = [str(player.name), self.course.name, self.course.layout, date, player.total, player.score]
            for score in player.holes:
                player_csv.append(score)
            data.append(player_csv)
        return header, data

    def get_embed(self, thumbnail=LOGO_URL):
        embed = self.get_small_embed(thumbnail)
        embed.color = 0xf17125
        if validate_embed(embed):
            return embed
        return None
