import json
from pathlib import Path
from .config import Config
from .clubplayerconfig import ClubPlayerConfig

class ClubConfig(Config):
    """DiscordUserConfig class, inherit to include discorduser configuration"""
    def __init__(self, server, discgolfmetrix_id:int, path:Path=None, module_name=None, file=None):
        super().__init__(server, path, module_name, file)
        self.discgolfmetrix_id:int = discgolfmetrix_id
        self.clubplayer_config:ClubPlayerConfig = []

    def create_module(self):
        """Create array configuration for the module"""
        return self.write([], self.module_name)

    def add_player(self, player):
        """Add a ClubPlayer instance to the list."""
        self.clubplayer_config.append(player)

    def to_dict(self):
        """Convert the object to a dictionary."""
        return {
            "ClubConfig": {
                "discgolfmetrix_id": self.discgolfmetrix_id,
                "ClubPlayers": [player.to_dict() for player in self.clubplayer_config]
            }
        }

    def to_json(self):
        """Convert the configuration to JSON."""
        return json.dumps(self.to_dict(), indent=4)
