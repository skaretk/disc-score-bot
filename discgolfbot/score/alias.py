import os.path
import json
from .player import PlayerName

class Alias:
    def __init__(self, server):
        self.server = server
        self.file = "alias.json"
        self.alias_list = []

    def parse(self):
        if os.path.isfile(f'{os.getcwd()}/cfg/{self.server}/{self.file}') is False:
            print(f'No Aliases stored for {self.server}')
            return

        with open(f'{os.getcwd()}/cfg/{self.server}/{self.file}', encoding='UTF-8', newline='') as json_file:
            data = json.load(json_file)
            for aliases in data['aliases']:
                self.alias_list.append(PlayerName(aliases.get('name'), aliases.get('alias')))

    def get_player_with_alias(self, player_name):
        for player in self.alias_list:
            if player.name == player_name:
                return player
            else:
                for alias in player.alias:
                    if alias == player_name:
                        return player
        return None

    def set_player_alias(self, player, new_alias):
        pass
