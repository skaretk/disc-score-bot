from dataclasses import dataclass
from typing import Optional

@dataclass(kw_only=True)
class Identifiers:
    """Common properties for Player"""
    pdga_number: Optional[int] = None
    discgolfmetrix_code: Optional[str] = None

    def __post_init__(self):
        if self.pdga_number is not None:
            if self.pdga_number not in range(1,500000):
                raise ValueError("Pdga number must between 1 <-> 499999")
