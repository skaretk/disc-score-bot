from .player import PlayerAlias
from .aliasconfig import AliasConfig

class Alias:
    """Alias Class, wrapper to read out and get players with aliases"""
    def __init__(self, server):
        self.server = server
        self.cfg = AliasConfig(server)
        self._alias_list = None

    @property
    def alias_list(self):
        """Returns a list of NameWithAlias objects with stored aliases, read out once"""
        if self._alias_list is None:
            json_object = self.cfg.read(self.cfg.module_name)
            if json_object is not None:
                alias_list = []
                for alias in json_object:
                    alias_list.append(PlayerAlias.from_json(alias))
                if alias_list:
                    self._alias_list = alias_list
        return self._alias_list

    def get_player_with_alias(self, name) -> PlayerAlias:
        """Return the Name of the player with aliases"""
        if self.alias_list:
            for alias in self.alias_list:
                if alias.name.lower() == name.lower() or alias.has_alias(name):
                    return alias
        return None
