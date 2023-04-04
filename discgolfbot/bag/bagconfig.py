from config import Config

class BagConfig(Config):
    '''Bag Config'''
    def __init__(self, server):
        super().__init__(server, "bag.json")

    def get_player_bag(self, player):
        '''Return the player bag url'''
        if self.config_exists() is False:
            print(f'No Config stored for {self.server}')
            return None

        json = self.read()
        for bag in json['bags']:
            if bag.get('user').lower() == player.lower():
                return bag.get('bag')

        return None

    def add_player_bag(self, player, url):
        '''Add the player bag. Return True if url is modifed, false otherwise'''
        json = self.read()

        modified = False
        if json:
            for bag in json['bags']:
                if bag.get('user').lower() == player.lower():
                    bag['bag'] = url
                    modified = True
                    break
            if modified is False:
                json['bags'].append({'user':player, 'bag':url})
        else: # Create new cfg
            json = {'bags':[{'user':player, 'bag':url}]}

        self.write(json)
        return modified

    def remove_player_bag(self, player):
        '''Remove the player bag. Return True if removed, False othervise'''
        if self.config_exists() is False:
            print(f'No Config stored for {self.server}')
            return False

        json = self.read()

        idx = None
        for i, bag in enumerate(json['bags']):
            if bag.get('user').lower() == player.lower():
                idx = i
                break

        if idx is None:
            return False

        del json['bags'][idx]
        self.write(json)
        return True