import json

class PlayerName:
    def __init__(self, name, alias = ''):
        self.name = name
        self.alias = alias

    def __eq__(self, other):
        if self.name.lower().replace(" ", "") == other.name.lower().replace(" ", ""):
            return True
        elif self.alias.lower().replace(" ", "") == other.name.lower().replace(" ", ""):
            return True
        else:
            return False