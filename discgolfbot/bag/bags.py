import json
import os.path
from collections import OrderedDict


class Bags:
    def __init__(self, server, user):
        self.cfg = f'{os.getcwd()}/cfg'
        self.server = server
        self.user = user
        self.file = "bags.json"

    def get_player_bag(self):
        if os.path.isfile(f'{self.cfg}/{self.server}/{self.file}') == False:
            print(f'No Bags stored for {self.server}')
            return None

        with open(f'{self.cfg}/{self.server}/{self.file}', encoding='UTF-8', newline='') as json_file:
            bags = json.load(json_file, object_pairs_hook=OrderedDict)
            for bag in bags['bags']:
                if (bag.get('user').lower() == self.user.lower()):
                    return bag.get('bag')
        return None

    def add_player_bag(self, bag_link):
        with open(f'{self.cfg}/{self.server}/{self.file}', 'r+', encoding='UTF-8', newline='', ) as json_file:
            bags = json.load(json_file)
            modified = False
            for bag in bags['bags']:
                if (bag.get('user').lower() == self.user.lower()):
                    bag['bag'] = bag_link
                    modified = True
                    break
            if (modified == False):
                bag = {'user': self.user, 'bag': bag_link}
                bags['bags'].append(bag)
            
            # rewind to top of the file
            json_file.seek(0)
            # sort_keys keeps the same order of the dict keys to put back to the file
            json.dump(bags, json_file, indent=4, sort_keys=False)
            # just in case your new data is smaller than the older
            json_file.truncate()
            return modified