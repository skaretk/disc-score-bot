import os
import discord
from discord.ext import commands
from discord.message import Attachment

# Fetch python bot token
from dotenv import load_dotenv
from os import getenv
load_dotenv('token.env')
token = getenv("TOKEN")

from csvreader import CsvReader
import utilities

# cogs
from attachment import Attachment
from scores import Scores
from emojis import Emojis
from files import Files

# discord client
bot = commands.Bot(command_prefix='%')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user} - {discord.__version__}')
    await bot.change_presence(activity=discord.Game(name="Disc golf"))

@bot.event
async def on_message(message):    
    await bot.process_commands(message)

@bot.command()
async def dates(ctx):

    path = str(f'{ctx.guild.name}\{ctx.channel}')

    if utilities.is_path_empty(path):
        await ctx.send("No scores stored for this channel")
        return
    
    # Get current dates
    datelist = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            csvreader = CsvReader(path, file)
            scorecard = csvreader.parse()

            date = scorecard.date_time.date()

            if date not in datelist:
                datelist.append(date)
    
    msg = ''
    for date in datelist:
        msg += f'\n{date}'

    await ctx.send(msg)

bot.add_cog(Attachment(bot))
bot.add_cog(Emojis(bot))
bot.add_cog(Files(bot))
bot.add_cog(Scores(bot))

bot.run(token)
