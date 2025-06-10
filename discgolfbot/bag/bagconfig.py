from pathlib import Path
from config import DiscordUserConfig

class BagConfig(DiscordUserConfig):
    """Bag Config"""
    def __init__(self, server, path:Path=None):
        super().__init__(server, path, module_name=__class__.__name__)

    def get_url(self, discord_id:int):
        """Return the users bag url"""
        user = self.get_user(discord_id)
        return user['url'] if user is not None else None
