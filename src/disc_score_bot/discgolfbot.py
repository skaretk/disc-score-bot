
import logging
from os import getenv

# nextcord
import nextcord
from dotenv import load_dotenv  # Fetch python bot token
from nextcord.ext import commands

# cogs
from .bag import Bag
from .discgolfmetrix import DiscgolfMetrix
from .discs import Discs
from .emoji import Emojis
from .logging_config import configure_logging
from .pdga import PdgaApprovedDiscs, PdgaPlayerStat
from .score import Scores

def main():
    """main() entrypoint - discord client """
    configure_logging()
    logger = logging.getLogger(__name__)
    cfg_dir = getenv("CFG_DIR", "cfg")
    load_dotenv(f'{cfg_dir}/token.env')
    token = getenv("TOKEN")

    # intents
    intents = nextcord.Intents.default()
    intents.typing = False
    intents.message_content = True

    bot = commands.Bot(command_prefix='%', intents=intents)

    @bot.event
    async def on_ready():
        logger.info('We have logged in as %s - %s', bot.user, nextcord.__version__)
        await bot.change_presence(activity=nextcord.Game(name="Disc golf"))

    @bot.event
    async def on_message(message):
        await bot.process_commands(message)

    bot.add_cog(Scores(bot))
    bot.add_cog(Emojis(bot))
    bot.add_cog(Discs(bot))
    bot.add_cog(Bag(bot))
    bot.add_cog(PdgaApprovedDiscs(bot))
    bot.add_cog(DiscgolfMetrix(bot))
    bot.add_cog(PdgaPlayerStat(bot))
    bot.run(token)

if __name__ == '__main__':
    main()
