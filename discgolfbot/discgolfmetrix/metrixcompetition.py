import json
from collections import OrderedDict
import nextcord
from apis.discgolfmetrixapi import metrix_favicon, metrix_logo

class MetrixCompetition:
    def __init__(self, json):
        self.json = json
        self.competition_url = f'https://discgolfmetrix.com/{self.get_id()}'
        self.error = json.get("Errors")
        self.name = self.get_name()
    
    def get_name(self):
        if self.json is not None:
            competition = self.json.get("Competition")
            name = competition.get("Name")
            if not name:
                return None
            return name
        return None
    
    def get_id(self):
        if self.json is not None:
            competition = self.json.get("Competition")
            name = competition.get("ID")
            if not name:
                return None
            return name
        return None
    
    def is_valid(self):
        if self.error is None and self.name is not None:
            return True
        return False
