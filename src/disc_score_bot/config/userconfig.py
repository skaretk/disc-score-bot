from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional
import logging
from .config import Config
from .identifiers import Identifiers

logger = logging.getLogger(__name__)

@dataclass
class User(Identifiers):
    """User Config"""
    discord_id : int
    bag_url : Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        if len(str(self.discord_id)) not in range(16,23):
            raise ValueError("Illegal discord user id")

class UserConfig(Config):
    """Handle UserConfig section of the JSON config"""
    def __init__(self, server, path: Path = None, module_name="UserConfig", file=None):
        super().__init__(server, path, module_name, file)

    def create_module(self):
        """Create empty array for UserConfig"""
        return self.write([], self.module_name)

    def _find_user_by(self, key: str, value: Any) -> Optional[User] | None:
        """Return the User whose dict[key] == value, or None."""
        data = self.read_module() or []
        for p in data:
            if p.get(key) == value:
                return User(**p)
        return None

    def get_user(self, discord_id: int) -> Optional[User] | None:
        """Lookup User by discord id"""
        return self._find_user_by("discord_id", discord_id)

    def get_user_by_pdga_number(self, pdga_number: int) -> Optional[User] | None:
        """Lookup User by pdga number [Optional]"""
        return self._find_user_by("pdga_number", pdga_number)

    def get_user_by_discgolfmetrix_code(self, discgolfmetrix_code: str) -> Optional[User] | None:
        """Lookup User by discgolfmetrix code [Optional]"""
        return self._find_user_by("discgolfmetrix_code", discgolfmetrix_code)

    def add_user(self, user: User) -> tuple[bool, bool]:
        """Add or edit a user"""
        json_object = self.read_module() or []

        user_dict = asdict(user)
        modified = False
        for p in json_object:
            if p["discord_id"] == user.discord_id:
                p.update(user_dict)
                modified = True
                break

        if not modified:
            json_object.append(user_dict)

        return self.write(json_object, self.module_name), modified

    def remove_user(self, discord_id: int):
        """Remove a user by discord_id"""
        cfg = self.read_module()
        if cfg is None:
            return False

        for i, p in enumerate(cfg):
            if p["discord_id"] == discord_id:
                del cfg[i]
                return self.write(cfg, self.module_name)

        return False
