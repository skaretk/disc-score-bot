
class PlayerAlias:
    """PlayerAlias class, contain player name with aliases"""
    def __init__(self, name:str, aliases:list=None):
        self.name = name
        self.aliases = aliases

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.name)

    def __eq__(self, other):
        if isinstance(other, PlayerAlias):
            if self.name.lower().replace(" ", "") == other.name.lower().replace(" ", ""):
                return True
            if self.aliases is not None:
                if self.has_alias(other.name):
                    return True
            elif other.aliases is not None:
                if other.has_alias(self.name):
                    return True
        return False

    @staticmethod
    def from_json(json_object):
        """Returns Name object from json object"""
        return PlayerAlias(json_object['name'], json_object['aliases'])

    def add_alias(self, alias):
        """Add new alias"""
        self.aliases.append(alias)

    def remove_alias(self, alias):
        """Remove alias"""
        self.aliases.remove(alias)

    def has_alias(self, name):
        """Check if the players has any aliases"""
        search_name = name.lower().replace(" ", "")
        if self.aliases is not None:
            if search_name in [alias.lower().replace(" ", "") for alias in self.aliases]:
                return True

        return False
