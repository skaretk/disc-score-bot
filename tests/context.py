import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../discgolfbot")))
print(sys.path)

import apis
import bag
import config
import discgolfmetrix
import discs
import discord_utils
import score
import scrapers