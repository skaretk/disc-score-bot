import json
from collections import OrderedDict
import nextcord
from apis.discgolfmetrixapi import metrix_favicon, metrix_logo
from .metrixcompetition import MetrixCompetition

class MetrixCompetitions:
    def __init__(self):
        self.competitions = []

    def add_competition(self, competition):
        self.competitions.append(competition)
        
    def get_embed(self):
        embed=nextcord.Embed(title="Competitions", description=f'Found {len(self.competitions)} Competitions:{self.format_competitions_description()}', color=0x004899)
        embed.set_footer(text="discgolfmetrix api", icon_url=metrix_favicon())
        return embed
    
    def format_competitions_description(self):
        description_text = ''
        for competition in self.competitions:
            description_text += f'\n[{competition.name}]({competition.competition_url})'
        return description_text