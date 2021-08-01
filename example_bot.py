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

# discord client
client = discord.Client()

class Player:
    def __init__(self, name, total, score):
        self.name = name
        self.total = total
        self.score = score

    def __str__(self):
     return f'Spiller: {self.name} Score: {self.score} Kast: {self.total}'

    #def __lt__(self, other):
    #    return True if self.score < other.score else False
  
    #def __le__(self, other):
    #    return True if self.score <= other.score else False
  
    #def __ne__(self, other):
    #    return True if self.score != other.score else False
  
    #def __gt__(self, other):
    #    return True if self.score > other.score else False
  
    #def __ge__(self, other):
    #    return True if self.score >= other.score else False
    
    def __eq__(self, other):
        return True if self.name == other.name else False
    
    def __add__(self, other):
        return Player(self.name, self.total + other.total, self.score + other.score)

class Scorecard:
    def __init__(self, coursename, date, total):
        self.coursename = coursename
        self.date = date
        self.total = total
        self.playerlist = []

    def __str__(self):
        msg = f'{self.coursename} Dato: {self.date} Par: {self.total}'
        for player in self.playerlist:
            msg += f'\n{player}'
        return msg

    def add_player(self, player):
        self.playerlist.append(player)

    def print(self):
        print(self)
    
    def sort_players_score(self):
        self.playerlist.sort(key=lambda x: x.score)
    
    def sort_players_total(self):
        self.playerlist.sort(key=lambda x: x.total)

    def print_players(self):        
        for player in self.playerlist:
            print(player)

class Scorecard_total:
    def __init__(self):
        self.scorecardlist = []
        self.playerlist = []
    
    def __str__(self):
        msg = f'Total Scores:'
        for player in self.playerlist:
            msg += f'\n{player}'
        return msg
    
    def add_scorecard(self, scorecard):
        self.scorecardlist.append(scorecard)
    
    def add_player(self, new_player):
        self.playerlist.append(new_player)
    
    def player_exist(self, new_player):
        if (new_player in self.playerlist):
            return True
        else:
            return False
    
    def sort_players_score(self):
        self.playerlist.sort(key=lambda x: x.score)

    def print_scores(self):
        print("Total Scores")
        for player in self.playerlist:
            print(player)
            

def parse_csv(path, filename):
    with open('{}\{}'.format(path, filename)) as csv_file:
        reader = csv.DictReader(csv_file)
        line_count = 0
        for row in reader:
            if line_count == 0:
                scorecard = Scorecard(row['CourseName'], row['Date'], int(row['Total']) )
            else:
                player = Player(row['PlayerName'], int(row['Total']), int(row['+/-']))
                scorecard.add_player(player)
            line_count += 1
        scorecard.sort_players_score()
        return scorecard


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
                with open('{}\{}'.format(currentPath, attachment.filename)) as csv_file:
                    reader = csv.DictReader(csv_file)
                    line_count = 0
                    for row in reader:
                        if line_count == 0:
                            scorecard = Scorecard(row['CourseName'], row['Date'], int(row['Total']) )
                        else:
                            player = Player(row['PlayerName'], int(row['Total']), int(row['+/-']))
                            scorecard.add_player(player)
                        line_count += 1
                    scorecard.print()
                    print("Normal print")
                    scorecard.print_players()
                    print("Print by score")
                    scorecard.sort_players_score()
                    scorecard.print_players()
                    msg_to_send = scorecard.coursename
                    for player in scorecard.playerlist:
                        msg_to_send += f'\n{player}'

                await message.channel.send(msg_to_send)

    # Check files stored for the current channel
    elif message.content == '%discbot files':        
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

    # Check current scores stored in this channel
    elif message.content == '%discbot scores':        
        if not os.path.exists(currentPath):
            await message.channel.send("No scores stored for this channel")
            return
        
        scorecard_total = Scorecard_total()
        for file in os.listdir(currentPath):
            if file.endswith(".csv"):
                scorecard = parse_csv(currentPath, file)
                scorecard_total.add_scorecard(scorecard)
                for player in scorecard.playerlist:
                    if scorecard_total.player_exist(player):
                        idx = scorecard_total.playerlist.index(player)
                        scorecard_total.playerlist[idx] += player
                    else:    
                        scorecard_total.add_player(player)
                #tmp print
                scorecard.sort_players_score()
                print(scorecard)
                
                await message.channel.send(f'Scorecard:\n{scorecard}')
        
        scorecard_total.sort_players_score()
        scorecard_total.print_scores()
        await message.channel.send(f'Total:\n{scorecard_total}')

client.run('ODY4MjAxODY0MDA3NjU5NTYx.YPsN_g.5gkeaR6HIzCjxIyMcgLksOoSbgk')
