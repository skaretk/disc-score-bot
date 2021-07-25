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
    author=str(message.author)
    if channel == "bot":
        if message.attachments:
            print("There is an attachment")            
            for attachment in message.attachments:
                print("{0} attached!".format(attachment.content_type))
                if 'text/csv' in attachment.content_type:
                    print("csv attached!")                    
                    await attachment.save(fp="csv/{}".format(attachment.filename)) # saves the file
                    await message.channel.send('.csv file {} received from {} and stored!'.format(attachment.filename, author))
                    print("csv attached and stored in csv/{}!".format(attachment.filename)) 

                    with open('csv/{}'.format(attachment.filename)) as csv_file:
                        reader = csv.DictReader(csv_file)
                        line_count = 0
                        message_to_send = ''
                        for row in reader:
                            if line_count == 0:
                                print("{} {} {}".format(row['CourseName'], row['Date'], row['Total'])) 
                                message_to_send += "{} {} {}\n".format(row['CourseName'], row['Date'], row['Total'])
                            else:
                                print("{} {} {}".format(row['PlayerName'], row['Total'], row['+/-']))
                                message_to_send += "\n{} {} {}".format(row['PlayerName'], row['Total'], row['+/-'])
                            line_count += 1
                        await message.channel.send(message_to_send)

                else:
                    print("Not a .csv?")
        else:
            print("There is no attachment")

#@client.event

client.run('ODY4MjAxODY0MDA3NjU5NTYx.YPsN_g.5gkeaR6HIzCjxIyMcgLksOoSbgk')

