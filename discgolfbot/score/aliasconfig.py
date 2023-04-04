from score.player import PlayerName
from config import Config

class AliasConfig(Config):
    '''Alias Config'''
    def __init__(self, server):
        super().__init__(server, "alias.json")

    def get_user_alias(self, player_name):
        '''Return the player aliases list, or None if player has no aliases stored'''
        if self.config_exists() is False:
            print(f'No Config stored for {self.server}')
            return None

        cfg = self.read()

        for player in cfg['aliases']:
            if player.get('name').lower() == player_name.lower():
                return PlayerName(player.get('name'), player.get('alias'))
            for alias in player.get('alias'):
                if alias == player_name:
                    return PlayerName(player.get('name'), player.get('alias'))
        return None

    def add_user_alias(self, player_name, new_alias):
        '''Add a new player player alias. Return True if added or modifed, false otherwise'''
        cfg = self.read()

        modified = False
        for player in cfg['aliases']:
            if player.get('name').lower() == player_name.lower(): # Found player
                for alias in player.get('alias'):
                    if alias == new_alias: # Already in the alias list
                        return False
                player_alias = {'alias':new_alias}
                player['alias'].append(player_alias)
                modified = True

        if modified is False:
            player_alias = {'name':player_name, 'alias':[new_alias]}

        self.write(cfg)
        return True

    def remove_user_alias(self, player_name, alias):
        '''Remove the player alias. Return True if removed, False othervise'''