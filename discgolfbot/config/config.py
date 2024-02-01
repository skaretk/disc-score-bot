from abc import abstractmethod
import json
from pathlib import Path

class Config:
    """Cfg class, handle bot configuration"""
    def __init__(self, server, module_name=None, file=None):
        self.server = server
        self.file = "config.json" if file is None else file
        self.module_name = module_name

    @property
    def path(self):
        """Get the config path"""
        return Path.cwd() / "cfg" / self.server

    @property
    def config(self):
        """Get the config filename"""
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

    def module_exists(self):
        """Check if the config contain module configuration"""
        if self.config_exists() is False:
            return False
        if self.module_name is not None:
            if self.read(self.module_name) is not None:
                return True
        return False

    def create(self):
        """Create the json file"""
        if self.path_exists() is False:
            self.path.mkdir()
        try:
            with open(self.config, 'w', encoding='UTF-8', newline='') as json_file:
                json.dump({}, json_file)
                return True
        except IOError:
            return False

    @abstractmethod
    def create_module(self):
        """Override in child class"""

    def read(self, module_name=None):
        """Returns the Config file as a json object"""
        try:
            with open(self.config, 'r', encoding='UTF-8', newline='') as json_file:
                cfg = json.load(json_file)
                if module_name is None:
                    return cfg
                return cfg[module_name] if module_name in cfg else None
        except IOError:
            return None

    def write(self, json_object, module_name=None):
        """Writes the Config file as a json object, returns True on success"""
        if self.path_exists() is False:
            self.path.mkdir()
        if self.config_exists() is False:
            self.create()

        data = self.read()
        if data is not None:
            try:
                with open(self.config, 'w', encoding='UTF-8', newline='') as json_file:
                    data[module_name] = json_object
                    json.dump(data, json_file, indent=4, sort_keys=False)
                    return True
            except IOError:
                print("Could not store the json")
        return False
