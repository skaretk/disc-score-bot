import json
from score.name import Name
from config import Config

class AliasConfig(Config):
    """Alias Config"""
    def __init__(self, server):
        super().__init__(server, "alias.json")

    def get_user_alias(self, user_name):
        """Return the json object from the alias list, or None if player has no aliases stored"""
        if self.config_exists() is False:
            print(f'No Config stored for {self.server}')
            return None

        json_object = self.read()

        for user in json_object['aliases']:
            if user.get('name').lower() == user_name.lower():
                return user
            if isinstance(user.get('alias'), list):
                for alias in user.get('alias'):
                    if alias.lower() == user_name.lower():
                        return user
        return None

    def add_user_alias(self, user_name, user_alias):
        """Add a new user alias to json. Return True if added or modifed, False otherwise"""
        json_object = self.read()

        alias_added = False
        if json_object:
            for user in json_object['aliases']:
                player_name = Name.from_json(user)
                if player_name.name.lower() == user_name.lower(): # Found player
                    if player_name.has_alias(user_alias):
                        return False # Already in the list
                    player_name.add_alias(user_alias)
                    user = json.dumps(player_name.__dict__, indent=4)
                    alias_added = True
        else: # Create new cfg
            json_object = {'aliases':[{'name':user_name, 'alias':[user_alias]}]}

        if alias_added is False:
            json_object['aliases'].append({'name':user_name, 'alias':[user_alias]})

        return self.write(json_object)

    def remove_user_alias(self, user_name, user_alias):
        """Remove the users alias. Return True if removed, False othervise"""
        json_object = self.read()

        alias_removed = False
        if json_object:
            for user in json_object['aliases']:
                player_name = Name.from_json(user)
                if player_name.name.lower() == user_name.lower(): # Found player
                    if player_name.has_alias(user_alias):
                        player_name.remove_alias(user_alias)
                        user = json.dumps(player_name.__dict__, indent=4)
                        alias_removed = True
                    break

        if alias_removed is False:
            return False

        return self.write(json_object)

    def remove_user(self, user_name):
        """Remove the user from the alias list. Return True if removed, False othervise"""
        if self.config_exists() is False:
            print(f'No Config stored for {self.server}')
            return False

        json_object = self.read()

        idx = None
        for i, user in enumerate(json_object['aliases']):
            if user.get('name').lower() == user_name.lower():
                idx = i
                break

        if idx is None:
            return False

        del json_object['aliases'][idx]
        self.write(json_object)
        return True
