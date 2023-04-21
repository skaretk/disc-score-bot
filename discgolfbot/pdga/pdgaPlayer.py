
class PdgaPlayer:
    def __init__(self, pdga_number, player_name, discord_id):
        self.player_name = player_name
        self.pdga_number = pdga_number
        self.discord_id = discord_id

    def to_dict(self):
        return {
                    "pdga_number":self.pdga_number,
                    "player_name":self.player_name,
                    "discord_id":self.discord_id
                }