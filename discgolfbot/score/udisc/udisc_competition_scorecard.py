import nextcord
from discord_utils.embed_validation import validate_embed
from score.scorecard import Scorecard

class UdiscScoreCardCompetition(Scorecard):
    """uDisc Scorecard Competition/League Class"""
    def __init__(self):
        super().__init__()
        self._name = None

    def __str__(self):
        return f'{self.date_time} - {self.name}'

    @property
    def name(self):
        """uDisc Competition/League Name"""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def append_field(self, embed=nextcord.Embed):
        embed.add_field(name=f'{self.date_time.date()} {self.name}', value=f'```{self.get_players_str()}```', inline=False)

    def get_small_embed(self, thumbnail=''):
        embed=nextcord.Embed(title=self.name, description=f'{self.date_time}', color=0x004899)
        for division in self.divisions:
            embed.add_field(name=f'{division}', value=f'```{self.get_players(division)}```', inline=False)
        if thumbnail != '':
            embed.set_thumbnail(url=thumbnail)

        return embed

    def get_csv(self):
        header = ["division", "position", "name", "relative_score", "total_score", "payout"]
        data = []
        # date = self.date_time.strftime('%Y-%m-%d')
        for hole in self.holes:
            header.append(f'hole_{hole}')

        for player in self.players:
            player_csv = [player.division, player.score_cards_position[0], str(player.name), player.score, player.total, player.payout]
            for score in player.holes:
                player_csv.append(score)
            data.append(player_csv)
        return header, data

    def get_embed(self, thumbnail=''):
        embed = self.get_small_embed(thumbnail)
        if validate_embed(embed):
            return embed
        return None
