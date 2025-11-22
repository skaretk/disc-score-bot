from dataclasses import dataclass

@dataclass
class PdgaPlayer:
    """Dataclass for PdgaPlayer
    discord_id: [17-18] characters
    pdga_number: between [1-499999]
    """
    discord_id:int # 18 characters #
    pdga_number:int

    def __post_init__(self):
        if self.pdga_number not in range(1,500000):
            raise ValueError("Pdga number must be from 1 to 499999")
        if len(str(self.discord_id)) not in range(16,23):
            raise ValueError("Illegal discord user id")
