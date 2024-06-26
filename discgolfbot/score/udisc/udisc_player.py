import math
from score.player import Player

class UdiscPlayer(Player):
    """uDisc Player"""

    def get_pdga_rating(self):
        """Calculate estimated pdga rating"""
        return int(423.41 * math.log(self.rating) - 1330.5)
