import nextcord
from nextcord.ext import commands
from nextcord.message import Attachment

# Fetch python bot token
from dotenv import load_dotenv, find_dotenv
from os import getenv

# cogs
from score.files.attachment import Attachment
from score import Scores
from emoji import Emojis
from discs import Discs, PdgaApprovedDiscs
from bag import Bag
from discgolfmetrix import Metrix

# discord client
def main():
    load_dotenv(find_dotenv('token.env'))
    token = getenv("TOKEN")

    bot = commands.Bot(command_prefix='%')

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user} - {nextcord.__version__}')
        await bot.change_presence(activity=nextcord.Game(name="Disc golf"))

    @bot.event
    async def on_message(message):    
        await bot.process_commands(message)

    bot.add_cog(Attachment(bot))
    bot.add_cog(Scores(bot))
    bot.add_cog(Emojis(bot))
    bot.add_cog(Discs(bot))
    bot.add_cog(Bag(bot))
    bot.add_cog(PdgaApprovedDiscs(bot))
    bot.add_cog(Metrix(bot))

    bot.run(token)

if __name__ == '__main__':
    main()
