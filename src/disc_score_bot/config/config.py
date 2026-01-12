from abc import abstractmethod
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class Config:
    """Cfg class, handle bot configuration"""
    def __init__(self, server, path:Path=None, module_name=None, file=None):
        self._path = Path.cwd() if path is None else path
        self.server = server
        self.file = "config.json" if file is None else file
        self.module_name = module_name

    @property
    def cfg_path(self):
        """Config Folder"""
        return self._path / "cfg"

    @property
    def path(self):
        """Get the config path"""
        if not self.cfg_path.exists():
            self.cfg_path.mkdir()
        return self.cfg_path / self.server

    @property
    def config(self):
        """Get the config filename"""
        return self.path / self.file

    def path_exists(self):
        """Check if the config folder exists for the server"""
        if not self.path.exists():
            logger.warning('No Config folder for %s', self.server)
            return False

        return True

    def config_exists(self):
        """Check if the config file exists for the server"""
        if not self.config.is_file():
            logger.warning('No %s stored for %s', self.file, self.server)
            return False

        return True

    def module_exists(self):
        """Check if the config contain module configuration"""
        if not self.config_exists():
            return False
        if self.module_name is not None:
            if self.read(self.module_name) is not None:
                return True
        return False

    def read_module(self):
        """Return module data if it exists, else None"""
        if not self.module_exists():
            logger.warning("No Config stored for %s for this server: %s", self.module_name, self.server)
            return None
        return self.read(self.module_name) or []

    def create(self):
        """Create the json file"""
        if not self.path_exists() :
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
                #return cfg[module_name] if module_name in cfg else None
                return cfg.get(module_name)
        except (IOError, json.JSONDecodeError):
            return None

    def write(self, json_object, module_name=None):
        """Writes the Config file as a json object, returns True on success"""
        if not self.path_exists():
            self.path.mkdir()
        if not self.config_exists():
            self.create()

        data = self.read() or {}
        try:
            with open(self.config, "w", encoding="UTF-8", newline="") as json_file:
                data[module_name] = json_object
                json.dump(data, json_file, indent=4, sort_keys=False)
                return True
        except IOError:
            logger.exception("Could not store the json")
            return False
