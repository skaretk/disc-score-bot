import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.resolve() / "discgolfbot"))
print(sys.path)

import apis
import bag
import config
import discgolfmetrix
import discs
import discord_utils
import score
import scrapers