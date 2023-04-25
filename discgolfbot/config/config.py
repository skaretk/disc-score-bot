from collections import OrderedDict
import json
from pathlib import Path

class Config:
    """Cfg class, handle the bot configuration"""
    def __init__(self, server, file=''):
        self.server = server
        self.file = file

    @property
    def path(self):
        """Get the config path"""
        return Path.cwd() / "cfg" / self.server

    @property
    def config(self):
        """Get the config file"""
        return self.path / self.file

    def path_exists(self):
        """Check if the config folder exists for the server"""
        if self.path.exists() is False:
            print(f'No Config folder for {self.server}')
            return False

        return True

    def config_exists(self):
        """Check if the config file exists for the server"""
        if self.config.is_file() is False:
            print(f'No {self.file} stored for {self.server}')
            return False

        return True

    def read(self):
        """Returns the Config file as a json object"""
        try:
            with open(self.config, encoding='UTF-8', newline='') as json_file:
                cfg = json.load(json_file, object_pairs_hook=OrderedDict)
            return cfg
        except IOError:
            return None

    def write(self, json_object):
        """Writes the Config file as a json object, returns True on success"""
        if self.path_exists() is False:
            self.path.mkdir()
        try:
            with open(self.config, 'w', encoding='UTF-8', newline='') as json_file:
                json.dump(json_object, json_file, indent=4, sort_keys=False)
                return True
        except IOError:
            print("Could not store the json")
            return False
