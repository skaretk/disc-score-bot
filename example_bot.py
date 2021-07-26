import os
import discord
import logging
import csv

# Set up logger
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# discord bot
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = str(message.channel)
    author = str(message.author)
    currentPath = str('{}\{}'.format(message.guild.name, channel))

    # any attachemtns in the message?
    if message.attachments:
        for attachment in message.attachments:
            if 'text/csv' in attachment.content_type:
                print("csv attached from server {} channel {}".format(message.guild.name, channel))
                if not os.path.exists(currentPath):
                    os.makedirs(currentPath)
                await attachment.save(fp="{}\{}".format(currentPath, attachment.filename)) # saves the file in a server/channel folder
                await message.channel.send('{} attached {}'.format(attachment.filename, author))
                print("csv attached and stored in {}\{}!".format(currentPath, attachment.filename)) 

                with open('{}\{}'.format(currentPath, attachment.filename)) as csv_file:
                    reader = csv.DictReader(csv_file)
                    line_count = 0
                    msg_to_send = ''
                    for row in reader:
                        if line_count == 0:
                            print("{} {} {}".format(row['CourseName'], row['Date'], row['Total'])) 
                            msg_to_send += "{} {} {}\n".format(row['CourseName'], row['Date'], row['Total'])
                        else:
                            print("{} {} {}".format(row['PlayerName'], row['Total'], row['+/-']))
                            msg_to_send += "\n{} {} {}".format(row['PlayerName'], row['Total'], row['+/-'])
                        line_count += 1
                await message.channel.send(msg_to_send)

    # Check status for the current channel
    elif message.content == '%status':        
        if not os.path.exists(currentPath):
            await message.channel.send("No files stored for this channel")
            return
        
        msg_to_send = ''
        file_count = 0
        for file in os.listdir(currentPath):
            if file.endswith(".csv"):
                file_count += 1
                print(os.path.join("{}\{}".format(currentPath, file)))
                msg_to_send += "\n{}".format(file)
        await message.channel.send("No of files: {}\n{}".format(file_count, msg_to_send))

#@client.event

client.run('ODY4MjAxODY0MDA3NjU5NTYx.YPsN_g.5gkeaR6HIzCjxIyMcgLksOoSbgk')
