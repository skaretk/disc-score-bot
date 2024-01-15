from dataclasses import dataclass

@dataclass
class PdgaPlayer:
    pdga_number:int
    player_name:str
    discord_id:int # 18 characters # 
    def __post_init__(self):
        if self.pdga_number not in range(1,500000): # 1-499999
            raise ValueError("Pdga number must be from 1 to 499999")
        if len(self.player_name) <=2:
            raise ValueError("Illegal player name. Player name must be at least 3 characters")
        if len(str(self.discord_id)) not in range(16,23): # discord id's usually consist of 18 numbers. So we ensure that the format looks kinda valid at least.
            raise ValueError("Illegal discord user id?")
