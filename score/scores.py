import os
from discord.ext import commands
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor
from score.files.scorecardreader import ScorecardReader
from score.files.scorecardwriter import ScorecardWriter
from score.alias import Alias
from score.scorecards import Scorecards
from scrapers.udisc import LeagueScraper
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

    def scrape(self, scraper_list):    
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=len(scraper_list)) as executor:
            for scraper in scraper_list:
                future = executor.submit(scraper.scrape)
        
        print(f'Spent {round(time.time() - start_time, 2)} scraping')

    # Checks
    def has_scorecards():
        def predicate(ctx):    
            if utilities.is_path_empty(f'{ctx.guild.name}\{ctx.channel}'):
                return False
            else:            
                return True
        return commands.check(predicate)

    @commands.group(pass_context=True, brief='Print stored scores', description='Prints all stored scorecards for this channel, including total')
    @has_scorecards()
    async def scores(self, ctx):    
        if ctx.invoked_subcommand is None:
            alias = Alias(ctx.guild.name)
            alias.parse()

            scorecards = get_scorecards(f'{ctx.guild.name}\{ctx.channel}', alias)

            if (scorecards.scorecards):
                embed = scorecards.get_embed(ctx.author.avatar_url)
                if (embed != None):
                    await ctx.send(embed=embed)
                else:
                    print("Embed not OK")
                    scorecards.save_scorecards_text(f'{ctx.guild.name}\{ctx.channel}\scores.txt')
                    await ctx.send('https://giphy.com/embed/32mC2kXYWCsg0')
                    await ctx.send(f'WOW {ctx.author.mention}, thats a lot of scores!)')                        
            else:
                await ctx.send("No courses found") 

    @scores.error
    async def scores_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('No scores stored for this channel')

    @scores.group(pass_context=True, brief='scores related to a course')
    async def course(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Missing subcommand, see %help scores course')
            return  

    @course.command(pass_context=True, name='list', brief='List courses', description='Lists courses stored in this channel')
    async def course_list(self, ctx):    
        course_list = []
        for file in os.listdir(f'{ctx.guild.name}\{ctx.channel}'):
            if file.endswith(".csv"):
                scorecard_reader = ScorecardReader(f'{ctx.guild.name}\{ctx.channel}', file)
                scorecard = scorecard_reader.parse()

                course_name = scorecard.coursename
                if course_name not in course_list:
                    course_list.append(course_name)
    
        msg = ''
        for course in course_list:
            msg += f'\n{course}'

        await ctx.send(msg)
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
            embed = scorecards.get_embed(ctx.author.avatar_url)
            if (embed != None):
                await ctx.send(embed=embed)
            else:
                print("Embed not OK")
                await ctx.send('https://giphy.com/embed/32mC2kXYWCsg0')
                await ctx.send(f'WOW {ctx.author.mention}, thats a lot of scores!)')
        else:
            await ctx.send("No courses found!")  

    @scores.group(pass_context=True, brief='scores related to dates')
    async def dates(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Missing subcommands, see %help scores dates')
            return 

    @dates.command(pass_context=True, name='list', brief='List dates', description='Lists all dates for scorecards stored in this channel')
    async def date_list(self, ctx):    
        date_list = []
        for file in os.listdir(f'{ctx.guild.name}\{ctx.channel}'):
            if file.endswith(".csv"):
                scorecard_reader = ScorecardReader(f'{ctx.guild.name}\{ctx.channel}', file)
                scorecard = scorecard_reader.parse()

                date = scorecard.date_time.date()
                if date not in date_list:
                    date_list.append(date)
    
        msg = ''
        for date in date_list:
            msg += f'\n{date}'

        await ctx.send(msg)
        pass
    
    @dates.command(pass_context=True, name='search', brief='Search for scorecards', description='Search and print scorecards for date(s) given\nSearch one date: 1.1.1990\nSearch between two dates: 1.1.1990 1.12.1990')
    async def dates_search(self, ctx, *args):
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
            embed = scorecards.get_embed(ctx.author.avatar_url)
            if (embed != None):
                await ctx.send(embed=embed)
            else:
                print("Embed not OK")
                await ctx.send('https://giphy.com/embed/32mC2kXYWCsg0')
                await ctx.send(f'WOW {ctx.author.mention}, thats a lot of scores!)')
        else:
            await ctx.send("No courses found")

    @commands.command(name='scores_stats', brief='statistics', description='Get statistics for saved scorecards')
    @has_scorecards()
    async def scores_stats(self, ctx):
        
        alias = Alias(ctx.guild.name)
        alias.parse()

        scorecards = get_scorecards(f'{ctx.guild.name}\{ctx.channel}', alias)

        if (scorecards.scorecards):
            embed = scorecards.get_embed_stats(ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No courses found")

    @commands.command(name='udiscleague', aliases=['uleague'], brief='uDiscLeague', description='Parse uDisc League')
    async def ukesgolf(self, ctx, *args,):
        if len(args) == 0:
            await ctx.send('No league specified, see %help udiscleague')
            return
        
        udisc_league = LeagueScraper(args[0])
        scraper_list = [udisc_league]
        self.scrape(scraper_list)

        date = udisc_league.score_card.date_time.strftime('%Y-%m-%d%H%M')
        file_name = f'{date}-{udisc_league.score_card.coursename}-{udisc_league.score_card.layoutname}-Udisc.csv'
        scorecard_writer = ScorecardWriter(str(f'{ctx.guild.name}\{ctx.channel}'), file_name)
        header, data = udisc_league.score_card.get_csv()
        scorecard_writer.write(header, data)


        embed = udisc_league.score_card.get_embed(ctx.author.avatar_url)
        if (embed != None):
            await ctx.send(embed=embed)
        else:
            ctx.send("Scorecard stored, but scores is to big to display!")
