from pathlib import Path
from config import DiscordUserConfig

class PdgaPlayerConfig(DiscordUserConfig):
    """PdgaPlayer Configuration"""
    def __init__(self, server, path:Path=None):
        super().__init__(server, path, module_name=__class__.__name__)

    def get_pdga_number(self, user_id:int):
        """Get player pdga number"""
        user = self.get_user(user_id)
        return user['pdga_number'] if user is not None else None
