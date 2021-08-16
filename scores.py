import os
from discord.ext import commands
from datetime import datetime

from scorecardreader import ScorecardReader
from alias import Alias
from scorecards import Scorecards
import utilities

def get_scorecards(path, alias):
    scorecards = Scorecards()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            scorecard_reader = ScorecardReader(path, file)
            scorecard = scorecard_reader.parse()

            scorecards.add_scorecard(scorecard, alias)

    return scorecards

def get_scorecards_course(path, alias, course):
    scorecards = Scorecards()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            scorecard_reader = ScorecardReader(path, file)
            scorecard = scorecard_reader.parse_course(course)
            if scorecard is not None:
                scorecards.add_scorecard(scorecard, alias)

    return scorecards

def get_scorecards_date(path, alias, date, date_to = ''):
    scorecards = Scorecards()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            scorecard_reader = ScorecardReader(path, file)
            scorecard = scorecard_reader.parse_dates(date, date_to)            

            if scorecard is not None:
                scorecards.add_scorecard(scorecard, alias)

    return scorecards

class Scores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    

    @commands.group(pass_context=True, brief='Print stored scores', description='Prints all stored scorecards for this channel, including total')
    async def scores(self, ctx):
        # Check current scores stored in this channel
        path = str(f'{ctx.guild.name}\{ctx.channel}')  
        if utilities.is_path_empty(path):
            await ctx.send('No scores stored for this channel')
            return
        
        alias = Alias(ctx.guild.name)
        alias.parse()

        if ctx.invoked_subcommand is None:
            scorecards = get_scorecards(path, alias)

            if (scorecards.scorecards):               
                await ctx.send(embed=scorecards.get_embed(ctx.author.avatar_url))  
            else:
                await ctx.send("No courses found")

    @scores.group(pass_context=True, brief='scores related to a course')
    async def course(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Missing subcommand, see %help scores course')
            return  

    @course.command(pass_context=True, name='list', brief='List courses', description='Lists courses stored in this channel')
    async def course_list(self, ctx):
        await ctx.send("Not implemented yet")
        pass

    @course.command(pass_context=True, name="search", brief='Search for scorecards for a course', description='Search and prints all scorecards for a course in this channel')
    async def search_course(self, ctx, arg = ''):
        if arg == '':
            await ctx.send('No course specified, see %help course search')
            return
            
        alias = Alias(ctx.guild.name)
        alias.parse()
    
        scorecards = get_scorecards_course(str(f'{ctx.guild.name}\{ctx.channel}'), alias, arg)           

        if (scorecards.scorecards):               
            await ctx.send(embed=scorecards.get_embed(ctx.author.avatar_url)) 
        else:
            await ctx.send("No courses found!")  

    @scores.group(pass_context=True, brief='scores related to dates')
    async def dates(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Missing subcommands, see %help scores dates')
            return 


    @dates.command(pass_context=True, name='list', brief='List dates', description='Lists all dates for scorecards stored in this channel')
    async def date_list(self, ctx):
        if utilities.is_path_empty(f'{ctx.guild.name}\{ctx.channel}'):
            await ctx.send("No scores stored for this channel")
            return
    
        datelist = []
        for file in os.listdir(f'{ctx.guild.name}\{ctx.channel}'):
            if file.endswith(".csv"):
                scorecard_reader = ScorecardReader(f'{ctx.guild.name}\{ctx.channel}', file)
                scorecard = scorecard_reader.parse()

                date = scorecard.date_time.date()

                if date not in datelist:
                    datelist.append(date)
    
        msg = ''
        for date in datelist:
            msg += f'\n{date}'

        await ctx.send(msg)
        pass        
    
    @dates.command(pass_context=True, name='search', brief='Search for scorecards', description='Search and print scorecards for date(s) given\nSearch one date: 1.1.1990\nSearch between two dates: 1.1.1990 1.12.1990')
    async def dates_search(self, ctx, *args):
        if utilities.is_path_empty(f'{ctx.guild.name}\{ctx.channel}'):
            await ctx.send("No scores stored for this channel")
            return

        if len(args) == 0:
            await ctx.send("Missing date(s)")
            return

        alias = Alias(ctx.guild.name)
        alias.parse()
        
        date = ''                
        try:
            date = datetime.strptime(args[0],'%d.%m.%Y')    
        except ValueError:
            await ctx.send("Invalid format in date 1 - should be 01.12.2021")
            return

        if len(args) == 1:
            scorecards = get_scorecards_date(str(f'{ctx.guild.name}\{ctx.channel}'), alias, date)
        if (len(args) > 1):
            date_to = ''
            try:
                date_to = datetime.strptime(args[1],'%d.%m.%Y')    
            except ValueError:
                await ctx.send("Invalid format in date 2 - should be 01.12.2021")
                return

            scorecards = get_scorecards_date(str(f'{ctx.guild.name}\{ctx.channel}'), alias, date, date_to)                                 

        if (scorecards.scorecards):               
            await ctx.send(embed=scorecards.get_embed(ctx.author.avatar_url)) 
        else:
            await ctx.send("No courses found")    
