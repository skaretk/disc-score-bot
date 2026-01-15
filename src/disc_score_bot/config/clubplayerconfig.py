from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional
import logging
from .config import Config
from .identifiers import Identifiers

logger = logging.getLogger(__name__)

@dataclass
class Player(Identifiers):
    """Player Config for Club"""
    name: str
    discord_id: Optional[int] = None

class ClubPlayerConfig(Config):
    """Handle ClubPlayerConfig section of the JSON config"""
    def __init__(self, server, path: Path = None, module_name="ClubPlayerConfig", file=None):
        super().__init__(server, path, module_name, file)

    def create_module(self):
        """Create empty array for ClubPlayerConfig"""
        return self.write([], self.module_name)

    def _find_player_by(self, key: str, value: Any) -> Optional[Player] | None:
        """Return the Player whose dict[key] == value, or None."""
        data = self.read_module() or []
        for p in data:
            if p.get(key) == value:
                return Player(**p)
        return None

    def get_player(self, name: str) -> Optional[Player] | None:
        """Lookup club_player by name"""
        return self._find_player_by("name", name)

    def get_player_by_discord_id(self, discord_id: int) -> Optional[Player] | None:
        """Lookup club_player by discord id [Optional]"""
        return self._find_player_by("discord_id", discord_id)

    def get_player_by_pdga_number(self, pdga_number: int) -> Optional[Player] | None:
        """Lookup club_player by pdg number"""
        return self._find_player_by("pdga_number", pdga_number)

    def get_player_by_discgolfmetrix_code(self, discgolfmetrix_code: str) -> Optional[Player] | None:
        """Lookup club_player by discgolfmetrix id [Optional]"""
        return self._find_player_by("discgolfmetrix_code", discgolfmetrix_code)

    def add_player(self, player: Player) -> tuple[bool, bool]:
        """Add or edit a player
        return:
        written: bool - config written
        modified: bool - config modified"""
        json_object = self.read_module() or []

        player_dict = asdict(player)
        modified = False
        for p in json_object:
            if p["name"] == player.name:
                p.update(player_dict)
                modified = True
                break

        if not modified:
            json_object.append(player_dict)

        return self.write(json_object, self.module_name), modified

    def remove_player(self, name: str) -> bool:
        """Remove a player by discord_id"""
        cfg = self.read_module()
        if cfg is None:
            return False

        for i, p in enumerate(cfg):
            if p["name"] == name:
                del cfg[i]
                return self.write(cfg, self.module_name)

        return False
