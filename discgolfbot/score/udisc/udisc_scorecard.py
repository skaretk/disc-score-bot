import dateutil.parser as dparser
import nextcord
from discord_utils.embed_validation import validate_embed
from score.scorecard import Scorecard

class UdiscScorecard(Scorecard):
    """uDisc Scorecard"""
    def __init__(self):
        super().__init__()
        self._date_time_end = None

    def __str__(self):
        return f'{self.date_time} - {self.course.name}: {self.course.layout}'

    @property
    def date_time_end(self):
        """Scorecard date end time"""
        return self._date_time_end

    @date_time_end.setter
    def date_time_end(self, date_time):
        try:
            self._date_time_end = dparser.parse(date_time, fuzzy=True)
        except dparser.ParserError:
            self._date_time_end = None

    @property
    def round_duration(self):
        """Scorecard duration - timedelta"""
        return self._date_time_end - self.date_time

    def append_field(self, embed=nextcord.Embed):
        embed.add_field(name=f'{self.course.name} ({self.course.layout}) {self.date_time.date()}', value=f'```{self.get_players()}```', inline=False)

    def get_csv(self):
        header = ['PlayerName', 'CourseName', 'LayoutName', 'StartDate', 'EndDate', 'Total', '+/-', 'RoundRating']
        data = []
        date = self.date_time.strftime('%Y-%m-%d %H:%M')
        date_end = self.date_time_end.strftime('%Y-%m-%d %H:%M')
        course_header = ['Par', self.course.name, self.course.layout, date, date_end, self.par, '', '']

        for hole in self.holes.items():
            header.append(f'Hole{hole}')
            course_header.append(hole)
        data.append(course_header)

        for player in self.players:
            player_csv = [str(player.name), self.course.name, self.course.layout, date, player.total, player.score, player.rating]
            for score in player.holes:
                player_csv.append(score)
            data.append(player_csv)
        return header, data

    def get_embed(self, thumbnail=''):
        """Get embed, include date start and end"""
        embed_title = self.course.name if self.course.name is not None else ''
        embed=nextcord.Embed(title=embed_title, url=self.course.url, description=f'{self.date_time.strftime("%Y.%m.%d %H:%M")} Start\n{self.date_time_end.strftime("%Y.%m.%d %H:%M")} End\nDuration: {self.round_duration}', color=0x004899)
        for division in self.divisions:
            embed.add_field(name=f'{division}', value=f'```{self.get_players(division)}```', inline=False)
        if thumbnail != '':
            embed.set_thumbnail(url=thumbnail)

        if validate_embed(embed):
            return embed
        return None
