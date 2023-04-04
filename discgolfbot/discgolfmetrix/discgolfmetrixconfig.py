from config import Config

class DiscgolfmetrixConfig(Config):
    '''Discgolfmetrix Configuration'''
    def __init__(self, server):
        super().__init__(server, "discgolfmetrix.json")

    def get_player_code(self, user):
        '''Get the users discgolfmetrix code'''
        if self.config_exists() is False:
            print(f'No Player Code stored for {self.server}')
            return None

        json_object = self.read()
        for player in json_object['metrix_players']:
            if player.get('user').lower() == user.lower():
                return player.get('code')

        return None

    def add_player_code(self, user, code):
        '''Add a player code'''
        json_object = self.read()

        modified = False
        if json_object:
            for player in json_object['metrix_players']:
                if player.get('user').lower() == user.lower():
                    player['code'] = code
                    modified = True
                    break
            if modified is False:
                json_object['metrix_players'].append({'user':user, 'code':code})

        self.write(json_object)
        return modified