import os
import discord
from discord.ext import commands

# Fetch python bot token
from dotenv import load_dotenv
from os import getenv
load_dotenv('token.env')
token = getenv("TOKEN")

from csv_reader import Csv_reader
from player import Player
from scorecard import Scorecard
from scorecard_total import Scorecard_total

# discord client
bot = commands.Bot(command_prefix='%')

def is_path_empty(path):
    if os.path.exists(path) and not os.path.isfile(path):  
        if not os.listdir(path):
            # Empty directory
            return True
        else:
            # Not empty directory
            return False
    else:
        # The path is either for a file or not valid
        return True

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="Disc golf"))

@bot.event
async def on_message(message):

    path = str(f'{message.guild.name}\{message.channel}')
    
    # any attachments in the message?
    if message.attachments:
        for attachment in message.attachments:
            if 'text/csv' in attachment.content_type:
                if not os.path.exists(path):
                    os.makedirs(path)
                await attachment.save(fp=f"{path}\{attachment.filename}") # saves the file in a server/channel folder
                await message.channel.send(f'{attachment.filename} attached by {message.author}')
                print(f'csv attached and stored in {path}\{attachment.filename}!')
                
                csv_reader = Csv_reader(path, attachment.filename)
                scorecard = csv_reader.parse()
                
                await message.channel.send(embed=scorecard.get_embed(message.author.avatar_url))
                await message.delete()
                return

    await bot.process_commands(message)

@bot.command()
async def files(ctx):

    path = str(f'{ctx.guild.name}\{ctx.channel}')

    if is_path_empty(path):
        await ctx.send('No files stored for this channel')
        return
        
    msg_to_send = ''
    file_count = 0
    for file in os.listdir(path):
        if file.endswith(".csv"):
            file_count += 1
            print(os.path.join(f'{path}\{file}'))
            msg_to_send += f'\n{file}'
    
    if file_count:     
        await ctx.send(f'No of files: {file_count}\n{msg_to_send}')
    else:
        await ctx.send('No .csv files stored for this channel')

@bot.command()
async def dates(ctx):

    path = str(f'{ctx.guild.name}\{ctx.channel}')

    if is_path_empty(path):
        await ctx.send("No scores stored for this channel")
        return
    
    # Get current dates
    datelist = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            csv_reader = Csv_reader(path, file)
            scorecard = csv_reader.parse()

            date = scorecard.date_time.date()

            if date not in datelist:
                datelist.append(scorecard.date_time.date())
    
    msg = ''
    for date in datelist:
        msg += f'\n{date}'

    await ctx.send(msg)

@bot.command()
async def scores(ctx):

    path = str(f'{ctx.guild.name}\{ctx.channel}')

    # Check current scores stored in this channel
    if is_path_empty(path):
        await ctx.send('No scores stored for this channel')
        return
    
    scorecard_total = Scorecard_total()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            csv_reader = Csv_reader(path, file)
            scorecard = csv_reader.parse()

            scorecard_total.add_scorecard(scorecard)
            for player in scorecard.playerlist:
                if scorecard_total.player_exist(player):
                    idx = scorecard_total.playerlist.index(player)
                    scorecard_total.playerlist[idx] += player
                else:
                    scorecard_total.add_player(player)
    
    scorecard_total.sort_players()
    scorecard_total.print_scores()

    await ctx.send(embed=scorecard_total.get_embed(ctx.author.avatar_url))  

bot.run(token)
