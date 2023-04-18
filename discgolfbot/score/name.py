
class Name:
    """Name class, contain name and aliases"""
    def __init__(self, name:str, alias:list=None):
        self.name = name
        self.alias = alias

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.name)

    def __eq__(self, other):
        if self.name.lower().replace(" ", "") == other.name.lower().replace(" ", ""):
            return True
        if self.alias is not None:
            if self.has_alias(other.name):
                return True
        elif other.alias is not None:
            if other.has_alias(self.name):
                return True
        return False

    @staticmethod
    def from_json(json_object):
        """Returns Name object from json object"""
        return Name(json_object['name'], json_object['alias'])

    def add_alias(self, alias):
        """Add new alias"""
        self.alias.append(alias)

    def remove_alias(self, alias):
        """Remove alias"""
        self.alias.remove(alias)

    def has_alias(self, name):
        """Check if the players has any aliases"""
        search_name = name.lower().replace(" ", "")
        if self.alias is not None:
            if search_name in [alias.lower().replace(" ", "") for alias in self.alias]:
                return True

        return False
