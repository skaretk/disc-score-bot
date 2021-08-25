import discord
from discord.ext import commands
from discord.message import Attachment

# Fetch python bot token
from dotenv import load_dotenv
from os import getenv
load_dotenv('token.env')
token = getenv("TOKEN")

# cogs
from attachment import Attachment
from scores import Scores
from emojis import Emojis
from files import Files
from discs import Discs
from flight import Flight

# discord client
bot = commands.Bot(command_prefix='%')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user} - {discord.__version__}')
    await bot.change_presence(activity=discord.Game(name="Disc golf"))

@bot.event
async def on_message(message):    
    await bot.process_commands(message)

bot.add_cog(Attachment(bot))
bot.add_cog(Scores(bot))
bot.add_cog(Emojis(bot))
bot.add_cog(Files(bot))
bot.add_cog(Discs(bot))
bot.add_cog(Flight(bot))

bot.run(token)
