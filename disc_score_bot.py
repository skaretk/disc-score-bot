import os
import discord
import logging

from csv_reader import Csv_reader
from player import Player
from scorecard import Scorecard
from scorecard_total import Scorecard_total

# Set up logger
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# discord client
client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')    

@client.event
async def on_message(message):
    if message.author == client.user:
       return

    channel = str(message.channel)
    author = str(message.author)
    currentPath = str(f'{message.guild.name}\{channel}')

    # any attachments in the message?
    if message.attachments:
        for attachment in message.attachments:
            if 'text/csv' in attachment.content_type:
                print("csv attached from server {} channel {}".format(message.guild.name, channel))
                if not os.path.exists(currentPath):
                    os.makedirs(currentPath)
                await attachment.save(fp="{}\{}".format(currentPath, attachment.filename)) # saves the file in a server/channel folder
                await message.channel.send('{} attached {}'.format(attachment.filename, author))
                print("csv attached and stored in {}\{}!".format(currentPath, attachment.filename))
                
                csv_reader = Csv_reader(currentPath, attachment.filename)
                scorecard = csv_reader.parse()

                await message.channel.send(scorecard)

    # Check files stored for the current channel
    elif message.content == '%scorebot files':        
        if not os.path.exists(currentPath):
            await message.channel.send("No files stored for this channel")
            return
        
        msg_to_send = ''
        file_count = 0
        for file in os.listdir(currentPath):
            if file.endswith(".csv"):
                file_count += 1
                print(os.path.join(f'{currentPath}\{file}'))
                msg_to_send += f'\n{file}'
        await message.channel.send(f'No of files: {file_count}\n{msg_to_send}')

    # Get current dates
    elif message.content == '%scorebot date':
        if not os.path.exists(currentPath):
            await message.channel.send("No scores stored for this channel")
            return
        datelist = []

        for file in os.listdir(currentPath):
            if file.endswith(".csv"):
                csv_reader = Csv_reader(currentPath, file)
                scorecard = csv_reader.parse()

                date = scorecard.date_time.date()

                if date not in datelist:
                    datelist.append(scorecard.date_time.date())
        
        msg = ''
        for date in datelist:
            msg += f'\n{date}'

        await message.channel.send(msg)

    # Check current scores stored in this channel
    elif message.content == '%scorebot scores':
        if not os.path.exists(currentPath):
            await message.channel.send("No scores stored for this channel")
            return
        
        scorecard_total = Scorecard_total()
        for file in os.listdir(currentPath):
            if file.endswith(".csv"):
                csv_reader = Csv_reader(currentPath, file)
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

        embed=discord.Embed(title="Disc-Score-Bot", url="", description="", color=0xFF5733)
        for scorecard in scorecard_total.scorecardlist:
            embed.add_field(name=scorecard.coursename, value=f'{scorecard.date_time.date()} Par:{scorecard.par}\n{scorecard.get_players()}', inline=True)    
        embed.add_field(name="Total", value=scorecard_total, inline=False)
        await message.channel.send(embed=embed)   

client.run('')
