from .player import Name
from .aliasconfig import AliasConfig

class Alias:
    """Alias Class, read and get players with aliases"""
    def __init__(self, server):
        self.server = server
        self.cfg = AliasConfig(server)
        self._alias_list = []

    @property
    def alias_list(self):
        """Returns a list of Name objects with stored aliases, read out once"""
        if not self._alias_list:
            json_object = self.cfg.read()
            if json_object is not None:
                alias_list = []
                for alias in json_object['aliases']:
                    alias_list.append(Name.from_json(alias))
                if alias_list:
                    self._alias_list = alias_list
        return self._alias_list

    def get_player_with_alias(self, name) -> Name:
        """Return the Name of the player with aliases"""
        if self.alias_list:
            for alias in self.alias_list:
                if alias.name.lower() == name.lower() or alias.has_alias(name):
                    return alias
        return None
