from collections import OrderedDict
import os
import json
from pathlib import Path

class Config:
    '''Cfg class, handle the bot configuration'''
    def __init__(self, server):
        self.path = Path(f'{os.getcwd()}/cfg/{server}')
        self.file = "cfg.json"
        self.server = server

    def exists(self):
        '''Check if the config file exists for the server'''
        if os.path.isfile(f'{self.path}/{self.file}') is False:
            print(f'No Config stored for {self.server}')
            return False

        return True

    def json(self):
        '''Returns the Config file as json'''
        try:
            with open(f'{self.path}/{self.file}', encoding='UTF-8', newline='') as json_file:
                cfg = json.load(json_file, object_pairs_hook=OrderedDict)
            return cfg
        except IOError:
            return None
