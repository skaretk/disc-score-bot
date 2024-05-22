from os import getenv
from dotenv import load_dotenv, find_dotenv # Fetch python bot token

# nextcord
import nextcord
from nextcord.ext import commands

# cogs
from score import Scores
from emoji import Emojis
from discs import Discs, PdgaApprovedDiscs
from bag import Bag
from discgolfmetrix import DiscgolfMetrix
from pdga import PdgaPlayerStat

# discord client
def main():
    load_dotenv(find_dotenv('cfg/token.env'))
    token = getenv("TOKEN")

    # intents
    intents = nextcord.Intents.default()
    intents.typing = False
    intents.message_content = True

    bot = commands.Bot(command_prefix='%', intents=intents)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user} - {nextcord.__version__}')
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
