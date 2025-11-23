from pathlib import Path
import logging
from .config import Config

logger = logging.getLogger(__name__)

class ClubPlayerConfig(Config):
    """Handle ClubPlayerConfig section of the JSON config"""

    def __init__(self, server, path: Path = None, module_name="ClubPlayerConfig", file=None):
        super().__init__(server, path, module_name, file)

    def create_module(self):
        """Create empty array for ClubPlayerConfig"""
        return self.write([], self.module_name)

    def get_player(self, discord_id: int = 0, name: str = None, pdga_number: int = 0, discgolfmetrix_id: int = 0):
        """Lookup a clubpPlayer.

        Args:
            discord_id, name, pdga_number, discgolfmetrix_id

        Returns:
            player_obj: object with .discord_id, .name, .pdga_number, .discgolfmetrix_id or None
        """
        if not self.module_exists():
            logger.warning("No Config stored for %s for this server: %s", self.module_name, self.server)
            return None

        json_object = self.read(self.module_name)
        if discord_id:
            return next((p for p in json_object if p["discord_id"] == discord_id), None)
        if name is not None:
            return next((p for p in json_object if p["name"] == name), None)
        if pdga_number:
            return next((p for p in json_object if p["pdga_number"] == pdga_number), None)
        if discgolfmetrix_id:
            return next((p for p in json_object if p["discgolfmetrix_id"] == discgolfmetrix_id), None)

    def add_player(self, player_obj):
        """Add or edit a player.

        Args:
            player_obj: object with .discord_id, .name, .pdga_number, .discgolfmetrix_id

        Returns:
            (written: bool, modified: bool)
        """
        if not hasattr(player_obj, "discord_id"):
            return False, False

        json_object = self.read(self.module_name) or []

        modified = False
        for p in json_object:
            if p["discord_id"] == player_obj.discord_id:
                p.update(player_obj.__dict__)
                modified = True
                break

        if not modified:
            json_object.append(player_obj.__dict__)

        return self.write(json_object, self.module_name), modified

    def remove_player(self, discord_id: int):
        """Remove a player by discord_id"""
        if not self.module_exists():
            logger.warning("No Config stored for %s for this server: %s", self.module_name, self.server)
            return False

        cfg = self.read(self.module_name)
        for i, p in enumerate(cfg):
            if p["discord_id"] == discord_id:
                del cfg[i]
                return self.write(cfg, self.module_name)

        return False
