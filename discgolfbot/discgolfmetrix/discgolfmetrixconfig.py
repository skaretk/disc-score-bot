from config import DiscordUserConfig

class DiscgolfmetrixConfig(DiscordUserConfig):
    """Discgolfmetrix Configuration"""
    def __init__(self, server):
        super().__init__(server, module_name=__class__.__name__)

    def get_code(self, discord_id:int):
        """Get the users discgolfmetrix code"""
        user = self.get_user(discord_id)
        return user['code'] if user is not None else None
