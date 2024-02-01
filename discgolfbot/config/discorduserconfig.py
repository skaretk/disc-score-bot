from . import Config

class DiscordUserConfig(Config):
    """DiscordUserConfig class, inherit to include discorduser configuration"""
    def __init__(self, server, module_name, file=None):
        super().__init__(server, module_name, file)

    def create_module(self):
        """Create array configuration for the module"""
        return self.write([], self.module_name)

    def get_user(self, discord_id:int):
        """Get the discord user in json config.

        Args:
            discord_id (int): The id to lookup

        Returns:
            object: discord_user or None if not found
        """
        if self.module_exists() is False:
            print(f'No Config stored for {self.module_name} for this server: {self.server}')
            return None

        json_object = self.read(self.module_name)
        return next((player for player in json_object if player['discord_id'] == discord_id), None)

    def add_user(self, discord_user):
        """Add or edit the discord_user.

        Args:
            discord_user (object): Object that contain .discord_id

        Returns:
                Boolean: Written
                Boolead: Modified
        """
        if hasattr(discord_user, 'discord_id') is False:
            return False, False
        json_object = self.read(self.module_name)

        modified = False
        if json_object is not None:
            for user in json_object:
                if user['discord_id'] == discord_user.discord_id:
                    user.update(discord_user.__dict__)
                    modified = True
                    break
            if modified is False:
                json_object.append(discord_user.__dict__)
        else: # Create new cfg
            json_object = [discord_user.__dict__]

        return self.write(json_object, self.module_name), modified

    def remove_user(self, discord_id:int):
        """Remove the userfrom json configuration.

        Args:
            discord_id (int): users discord id.

        Returns
            Bool: True if removed, else False
        """
        if self.module_exists() is False:
            print(f'No Config stored for {self.module_name} for this server: {self.server}')
            return False

        cfg = self.read(self.module_name)
        for i, j in enumerate(cfg):
            if j['discord_id'] == discord_id:
                del cfg[i]
                return self.write(cfg, self.module_name)

        return False
