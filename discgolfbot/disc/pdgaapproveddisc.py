from .disc import Disc

class PdgaApprovedDisc(Disc):
    """Pdga approved disc"""
    def __init__(self):
        super().__init__()
        self.manufacturer_url = ''
        self.approved_date = ''

    def __eq__(self, other):
        if self.name.lower() == other.name.lower() and self.manufacturer.lower() == other.manufacturer.lower() and self.approved_date.lower() == other.approved_date.lower() and self.url.lower() == other.url.lower():
            return True
        return False
