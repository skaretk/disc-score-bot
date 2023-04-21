import nextcord
from apis.discgolfmetrixapi import metrix_favicon

class DiscgolfmetrixCompetitions:
    """Discgolfmetrix competitions"""
    def __init__(self):
        self.competitions = []

    def add_competition(self, competition):
        """Add a competition"""
        self.competitions.append(competition)
        self.competitions.sort()

    def get_embed(self):
        """Get Embed"""
        embed=nextcord.Embed(title=f'Found {len(self.competitions)} {"Competition" if len(self.competitions) <= 1 else "Competitions"}', description=f'{self.format_competitions_description()}', color=0x004899)
        embed.set_footer(text="discgolfmetrix", icon_url=metrix_favicon())
        return embed

    def format_competitions_description(self):
        """Format embed description text"""
        description_text = ''
        for competition in self.competitions:
            description_text += f'\n{competition.datetime.strftime("%Y-%m-%d")} [{competition.name}]({competition.competition_url})'
        return description_text
