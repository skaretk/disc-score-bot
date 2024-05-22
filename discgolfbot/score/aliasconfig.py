import json
from score.playeralias import PlayerAlias
from config import Config

class AliasConfig(Config):
    """Alias Config"""
    def __init__(self, server):
        super().__init__(server, module_name=__class__.__name__)

    def create_module(self):
        """Create configuration for bag configuration"""
        return self.write([], self.module_name)

    def get_user_alias(self, user_name):
        """Return the json object from the alias list, or None if player has no aliases stored"""
        if self.module_exists() is False:
            print(f'No Config stored for {self.server}')
            return None

        json_object = self.read(self.module_name)

        for i in json_object:
            if i['name'].lower() == user_name.lower():
                return i
            for alias in i['aliases']:
                if alias.lower() == user_name.lower():
                    return i
        return None

    def add_user_alias(self, user_name, user_alias):
        """Add a new user alias to json. Return True if added or modifed, False otherwise"""
        json_object = self.read(self.module_name)

        alias_added = False
        if json_object is not None:
            for user in json_object:
                player_name = PlayerAlias.from_json(user)
                if player_name.name.lower() == user_name.lower(): # Found player
                    if player_name.has_alias(user_alias):
                        return False # Already in the list
                    player_name.add_alias(user_alias)
                    user = json.dumps(player_name.__dict__)
                    alias_added = True
            if alias_added is False:
                json_object.append({'name':user_name, 'aliases':[user_alias]})
        else: # Create new cfg
            json_object = [{'name':user_name, 'aliases':[user_alias]}]

        return self.write(json_object, self.module_name)

    def remove_user_alias(self, user_name, user_alias):
        """Remove the users alias. Return True if removed, False othervise"""
        json_object = self.read(self.module_name)

        if json_object:
            for user in json_object:
                player_name = PlayerAlias.from_json(user)
                if player_name.name.lower() == user_name.lower(): # Found player
                    if player_name.has_alias(user_alias):
                        player_name.remove_alias(user_alias)
                        user = json.dumps(player_name.__dict__, indent=4)
                        return self.write(json_object, self.module_name)

        return False

    def remove_user(self, user_name):
        """Remove the user from the alias list.
        Return True if removed, False othervise
        """
        if self.module_exists() is False:
            print(f'No Alias Config stored for {self.server}')
            return False

        cfg = self.read(self.module_name)
        for i, j in enumerate(cfg):
            if j['name'].lower() == user_name.lower():
                del cfg[i]
                return self.write(cfg, self.module_name)

        return False
