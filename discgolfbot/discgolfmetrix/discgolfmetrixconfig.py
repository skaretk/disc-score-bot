from config import Config

class DiscgolfmetrixConfig(Config):
    '''Discgolfmetrix Configuration'''
    def __init__(self, server):
        super().__init__(server, "discgolfmetrix.json")

    def get_code(self, user:int):
        '''Get the users discgolfmetrix code'''
        if self.config_exists() is False:
            print(f'No Discgolfmetrix codes stored for {self.server}')
            return None

        json_object = self.read()
        for player in json_object['metrix_players']:
            if player.get('user') == user:
                return player.get('code')

        return None

    def add_code(self, user:int, code):
        '''Add the users discgolfmetrix code, return True if added, False if modified'''
        json_object = self.read()

        modified = False
        if json_object:
            for player in json_object['metrix_players']:
                if player.get('user') == user:
                    player['code'] = code
                    modified = True
                    break
            if modified is False:
                json_object['metrix_players'].append({'user':user, 'code':code})
        else: # Create new cfg
            json_object = {'metrix_players':[{'user':user, 'code':code}]}

        self.write(json_object)
        return modified

    def remove_code(self, user:int):
        '''Remove the users discgolfmetrix code. Return True if removed, False othervise'''
        if self.config_exists() is False:
            print(f'No Config stored for {self.server}')
            return False

        json = self.read()

        idx = None
        for i, code in enumerate(json['metrix_players']):
            if code.get('user') == user:
                idx = i
                break

        if idx is None:
            return False

        del json['metrix_players'][idx]
        self.write(json)
        return True
