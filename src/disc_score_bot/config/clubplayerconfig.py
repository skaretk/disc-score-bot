from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
import logging
from .config import Config

logger = logging.getLogger(__name__)

@dataclass
class Player:
    """Player Config for Club"""
    pdga_number: int
    name: str
    discord_id: Optional[int] = None
    discgolfmetrix_id: Optional[int] = None

class ClubPlayerConfig(Config):
    """Handle ClubPlayerConfig section of the JSON config"""
    def __init__(self, server, path: Path = None, module_name="ClubPlayerConfig", file=None):
        super().__init__(server, path, module_name, file)

    def create_module(self):
        """Create empty array for ClubPlayerConfig"""
        return self.write([], self.module_name)

    def get_player_by_pdga_number(self, pdga_number: int) -> dict | None:
        """Lookup club_player by pdg number"""
        data = self.read_module()
        if data is None:
            return None
        return next((p for p in data if p.get("pdga_number") == pdga_number), None)

    def get_player_by_name(self, name: str) -> dict | None:
        """Lookup club_player by name"""
        data = self.read_module()
        if data is None:
            return None
        return next((p for p in data if p.get("name") == name), None)

    def get_player_by_discord_id(self, discord_id: int) -> dict | None:
        """Lookup club_player by discord id [Optional]"""
        data = self.read_module()
        if data is None:
            return None
        return next((p for p in data if p.get("discord_id") == discord_id), None)

    def get_player_by_discgolfmetrix_id(self, discgolfmetrix_id: int) -> dict | None:
        """Lookup club_player by discgolfmetrix id [Optional]"""
        data = self.read_module()
        if data is None:
            return None
        return next((p for p in data if p.get("discgolfmetrix_id") == discgolfmetrix_id), None)

    def add_player(self, player: Player) -> tuple[bool, bool]:
        """Add or edit a player"""
        json_object = self.read_module()
        if json_object is None:
            json_object = []

        player_dict = asdict(player)
        modified = False
        for p in json_object:
            if p["pdga_number"] == player.pdga_number:
                p.update(player_dict)
                modified = True
                break

        if not modified:
            json_object.append(player_dict)

        return self.write(json_object, self.module_name), modified

    def remove_player(self, pdga_number: int):
        """Remove a player by discord_id"""
        cfg = self.read_module()
        if cfg is None:
            return False

        for i, p in enumerate(cfg):
            if p["pdga_number"] == pdga_number:
                del cfg[i]
                return self.write(cfg, self.module_name)

        return False
