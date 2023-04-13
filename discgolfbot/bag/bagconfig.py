from config import Config

class BagConfig(Config):
    '''Bag Config'''
    def __init__(self, server):
        super().__init__(server, "bag.json")

    def get_bag(self, user:int):
        '''Return the users bag url'''
        if self.config_exists() is False:
            print(f'No Config stored for {self.server}')
            return None

        json = self.read()
        for bag in json['bags']:
            if bag.get('user') == user:
                return bag.get('url')

        return None

    def add_bag(self, user:int, url):
        '''Add the users bag. Return True if url is modifed, False otherwise'''
        json = self.read()

        modified = False
        if json:
            for bag in json['bags']:
                if bag.get('user') == user:
                    bag['url'] = url
                    modified = True
                    break
            if modified is False:
                json['bags'].append({'user':user, 'url':url})
        else: # Create new cfg
            json = {'bags':[{'user':user, 'url':url}]}

        self.write(json)
        return modified

    def remove_bag(self, user:int):
        '''Remove the users bag. Return True if removed, False othervise'''
        if self.config_exists() is False:
            print(f'No Config stored for {self.server}')
            return False

        json = self.read()

        idx = None
        for i, bag in enumerate(json['bags']):
            if bag.get('user') == user:
                idx = i
                break

        if idx is None:
            return False

        del json['bags'][idx]
        self.write(json)
        return True