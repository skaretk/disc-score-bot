import os
from discord.ext import commands
from datetime import datetime

from csvreader import CsvReader
from scorecards import Scorecards
import utilities

def get_scorecards(path):
    scorecards = Scorecards()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            csvreader = CsvReader(path, file)
            scorecard = csvreader.parse()

            scorecards.add_scorecard(scorecard)

    return scorecards

def get_scorecards_course(path, course):
    scorecards = Scorecards()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            csvreader = CsvReader(path, file)
            scorecard = csvreader.parse_course(course)
            if scorecard is not None:
                scorecards.add_scorecard(scorecard)

    return scorecards

def get_scorecards_date(path, date, date_to = ''):
    scorecards = Scorecards()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            csvreader = CsvReader(path, file)
            scorecard = csvreader.parse_dates(date, date_to)            

            if scorecard is not None:
                scorecards.add_scorecard(scorecard)

    return scorecards

class Scores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def scores(self, ctx, *args):  
        path = str(f'{ctx.guild.name}\{ctx.channel}')

        # Check current scores stored in this channel
        if utilities.is_path_empty(path):
            await ctx.send('No scores stored for this channel')
            return

        if args:
            print(f'%scores: {len(args)} arguments:', ', '.join(args))

            if args[0] == "course":
                if len(args) < 2:
                    ctx.send("Missing coursename")
                    return

                scorecards = get_scorecards_course(path, args[1])           

                if (scorecards.scorecardlist):               
                    await ctx.send(embed=scorecards.get_embed(ctx.author.avatar_url)) 
                else:
                    await ctx.send("No courses found")

            if args[0] == "date":
                if len(args) < 2:
                    ctx.send("Missing date")
                    return
            
                date = ''                
                try:
                    date = datetime.strptime(args[1],'%d.%m.%Y')    
                except ValueError:
                    await ctx.send("Invalid format in date 1 - should be 01.12.2021")
                    return

            if len(args) == 2:
                scorecards = get_scorecards_date(path, date)
            if (len(args) > 2):
                date_to = ''
                try:
                    date_to = datetime.strptime(args[2],'%d.%m.%Y')    
                except ValueError:
                    await ctx.send("Invalid format in date 2 - should be 01.12.2021")
                    return

                scorecards = get_scorecards_date(path, date, date_to)                                 

            if (scorecards.scorecardlist):               
                await ctx.send(embed=scorecards.get_embed(ctx.author.avatar_url)) 
            else:
                await ctx.send("No courses found")
            
        else: # no args, list all scores
            scorecards = get_scorecards(path)

            if (scorecards.scorecardlist):               
                await ctx.send(embed=scorecards.get_embed(ctx.author.avatar_url))  
            else:
                await ctx.send("No courses found")
