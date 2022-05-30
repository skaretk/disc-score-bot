import json
import os.path
from collections import OrderedDict

class MetrixPlayer:
    def __init__(self, server, user):
        self.cfg = f'{os.getcwd()}/cfg'
        self.server = server
        self.user = user
        self.file = "metrix.json"

    def get_player_code(self):
        if os.path.isfile(f'{self.cfg}/{self.server}/{self.file}') == False:
            print(f'No Player Code stored for {self.server}')
            return None

        with open(f'{self.cfg}/{self.server}/{self.file}', encoding='UTF-8', newline='') as json_file:
            metrix = json.load(json_file, object_pairs_hook=OrderedDict)
            for player in metrix['metrix_players']:
                if (player.get('user').lower() == self.user.lower()):
                    return player.get('code')
        return None

    def add_player_code(self, code):
        if os.path.isfile(f'{self.cfg}/{self.server}/{self.file}') == False:
            f = open(f'{self.cfg}/{self.server}/{self.file}',"w")
            f.close()

        with open(f'{self.cfg}/{self.server}/{self.file}', 'r+', encoding='UTF-8', newline='', ) as json_file:
            metrix = json.load(json_file)
            modified = False
            for player in metrix['metrix_players']:
                if (player.get('user').lower() == self.user.lower()):
                    player['code'] = code
                    modified = True
                    break
            if (modified == False):
                player = {'user': self.user, 'code': code}
                metrix['metrix_players'].append(player)
            
            # rewind to top of the file
            json_file.seek(0)
            # sort_keys keeps the same order of the dict keys to put back to the file
            json.dump(metrix, json_file, indent=4, sort_keys=False)
            # just in case your new data is smaller than the older
            json_file.truncate()
            return modified