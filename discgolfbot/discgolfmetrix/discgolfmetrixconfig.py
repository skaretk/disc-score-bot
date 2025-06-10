from pathlib import Path
from config import DiscordUserConfig

class DiscgolfmetrixConfig(DiscordUserConfig):
    """Discgolfmetrix Configuration"""
    def __init__(self, server, path:Path=None):
        super().__init__(server, path, module_name=__class__.__name__)

    def get_code(self, discord_id:int):
        """Get the users discgolfmetrix code"""
        user = self.get_user(discord_id)
        return user['code'] if user is not None else None
