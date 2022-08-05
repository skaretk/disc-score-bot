from concurrent.futures import ThreadPoolExecutor
from nextcord.ext import commands
from datetime import datetime
import os
import time
from scrapers.udisc import LeagueScraper
import utilities
from .files.members import Members
from .files.scorecardreader import ScorecardReader
from .files.scorecardwriter import ScorecardWriter
from .alias import Alias
from .point_system import calculate_player_score
from .scorecards import Scorecards

def get_scorecards(path, alias, member_list = None):
    scorecards = Scorecards()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            scorecard_reader = ScorecardReader(path, file)
            scorecard = scorecard_reader.parse()

            # Add aliases
            for player in scorecard.players:
                scorecards.add_player_alias(player, alias)

            # Check and remove players
            if member_list is not None:
                scorecard.players = [player for player in scorecard.players if player.player_name in member_list]
                scorecard.sort_players()
                scorecard.add_player_position()

            scorecards.add_scorecard(scorecard, alias)

    if member_list is not None:
        for player in scorecards.players:
            calculate_player_score(player, len(scorecards.scorecards))

    return scorecards

def get_scorecards_course(path, alias, course, member_list = None):
    scorecards = Scorecards()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            scorecard_reader = ScorecardReader(path, file)
            scorecard = scorecard_reader.parse_course(course)
            if scorecard is not None:
                # Add aliases
                for player in scorecard.players:
                    scorecards.add_player_alias(player, alias)

                # Check and remove players
                if member_list is not None:
                    scorecard.players = [player for player in scorecard.players if player.player_name in member_list]
                    scorecard.sort_players()
                    scorecard.add_player_position()

                scorecards.add_scorecard(scorecard, alias)

    if member_list is not None:
        for player in scorecards.players:
            calculate_player_score(player, len(scorecards.scorecards))

    return scorecards

def get_scorecards_date(path, alias, date, date_to = '', member_list = None):
    scorecards = Scorecards()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            scorecard_reader = ScorecardReader(path, file)
            scorecard = scorecard_reader.parse_dates(date, date_to)

            if scorecard is not None:
                # Add aliases
                for player in scorecard.players:
                    scorecards.add_player_alias(player, alias)

                # Check and remove players
                if member_list is not None:
                    scorecard.players = [player for player in scorecard.players if player.player_name in member_list]
                    scorecard.sort_players()
                    scorecard.add_player_position()

                scorecards.add_scorecard(scorecard, alias)

    if member_list is not None:
        for player in scorecards.players:
            calculate_player_score(player, len(scorecards.scorecards))

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
            if utilities.is_path_empty(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}'):
                return False
            else:
                return True
        return commands.check(predicate)

    @commands.group(pass_context=True, brief='scores [course / dates / files]', description='Prints scorecards for this channel')
    @has_scorecards()
    async def scores(self, ctx):
        if ctx.invoked_subcommand is None:
            print("Fetch Alias")
            alias = Alias(ctx.guild.name)
            alias.parse()
            print("Alias OK")

            if ("ukesgolf" in ctx.channel.name):
                print("ukesgolf")
                members = Members(f'{ctx.guild.name}', 'Medlemmer.xlsx')
                members.parse()
                scorecards = get_scorecards(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}', alias, members.member_list)
            else:
                print("NOT ukesgolf")
                scorecards = get_scorecards(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}', alias)

            if (scorecards.scorecards):
                if ("ukesgolf" in ctx.channel.name):
                    scorecards.sort_players_points()
                    embed = scorecards.get_embed_league(ctx.bot.user.avatar.url)

                else:
                    embed = scorecards.get_embed(ctx.author.avatar.url)

                if (embed != None):
                    await ctx.send(embed=embed)
                else:
                    print("Embed not OK")
                    scorecards.save_scorecards_text(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}/scores.txt')
                    await ctx.send('https://giphy.com/embed/32mC2kXYWCsg0')
                    await ctx.send(f'WOW {ctx.author.mention}, thats a lot of scores!)')
            else:
                await ctx.send("No courses found")

    @scores.error
    async def scores_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('No scores stored for this channel')

    @scores.command(brief='Print stored scorecards', description='Lists all scorecard files stored in this discord channel')
    async def files(self, ctx):
        path = str(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}')
        scorecards_text = ''
        file_count = 0
        for file in os.listdir(path):
            if file.endswith(".csv"):
                file_count += 1
                print(os.path.join(f'{path}/{file}'))
                scorecards_text += f'\n{file}'

        msg_to_send = f'No of files: {file_count}\n{scorecards_text}'

        if len(msg_to_send) > 2000:
            await ctx.send(f'No of files: {file_count}')
        elif file_count:
            await ctx.send(msg_to_send)
        else:
            await ctx.send('No .csv files stored for this channel')

    @scores.command(name='stats', brief='Print statistics', description='Print statistics for saved scorecards')
    async def stats(self, ctx):

        alias = Alias(ctx.guild.name)
        alias.parse()

        scorecards = get_scorecards(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}', alias)

        if (scorecards.scorecards):
            embed = scorecards.get_embed_stats(ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No courses found")

    @scores.group(pass_context=True, brief='[list / search]', description='List or search for courses')
    async def course(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Missing subcommand, see %help scores course')
            return

    @course.command(pass_context=True, name='list', brief='Print courses', description='Print stored courses in this channel')
    async def course_list(self, ctx):
        course_list = []
        for file in os.listdir(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}'):
            if file.endswith(".csv"):
                scorecard_reader = ScorecardReader(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}', file)
                scorecard = scorecard_reader.parse()

                course_name = scorecard.coursename
                if course_name not in course_list:
                    course_list.append(course_name)

        msg = ''
        for course in course_list:
            msg += f'\n{course}'

        await ctx.send(msg)
        pass

    @course.command(pass_context=True, name="search", brief='[Coursename]', description='Search and print scorecards for course')
    async def search_course(self, ctx, arg = ''):
        if arg == '':
            await ctx.send('No course specified, see %help course search')
            return

        alias = Alias(ctx.guild.name)
        alias.parse()

        if ("ukesgolf" in ctx.channel.name):
            members = Members(f'{os.getcwd()}/cfg/{ctx.guild.name}', 'Medlemmer.xlsx')
            members.parse()
            scorecards = get_scorecards_course(str(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}'), alias, arg, members.member_list)
        else:
            scorecards = get_scorecards_course(str(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}'), alias, arg)

        if (scorecards.scorecards):
            if ("ukesgolf" in ctx.channel.name):
                scorecards.sort_players_points()
                embed = scorecards.get_embed_league(ctx.bot.user.avatar.url)
            else:
                embed = scorecards.get_embed(ctx.author.avatar.url)

            if (embed != None):
                await ctx.send(embed=embed)
            else:
                print("Embed not OK")
                scorecards.save_scorecards_text(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}/scores.txt')
                await ctx.send('https://giphy.com/embed/32mC2kXYWCsg0')
                await ctx.send(f'WOW {ctx.author.mention}, thats a lot of scores!)')
        else:
            await ctx.send("No courses found!")

    @scores.group(pass_context=True, brief='[list / search]', description='List or search within dates')
    async def dates(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Missing subcommands, see %help scores dates')
            return

    @dates.command(pass_context=True, name='list', brief='Print stored dates', description='print all dates for scorecards stored in this channel')
    async def date_list(self, ctx):
        date_list = []
        for file in os.listdir(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}'):
            if file.endswith(".csv"):
                scorecard_reader = ScorecardReader(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}', file)
                scorecard = scorecard_reader.parse()

                date = scorecard.date_time.date()
                if date not in date_list:
                    date_list.append(date)

        msg = ''
        for date in date_list:
            msg += f'\n{date}'

        await ctx.send(msg)
        pass

    @dates.command(pass_context=True, name='search', brief='[1.1.2021 31.12.2021]', description='Search for scorecards within date(s) \search 1.1.1990\nsearch 1.1.1990 1.12.1990')
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
            if ("ukesgolf" in ctx.channel.name):
                members = Members(f'{ctx.guild.name}', 'Medlemmer.xlsx')
                members.parse()
                scorecards = get_scorecards_date(str(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}'), alias, date, '', members.member_list)
            else:
                scorecards = get_scorecards_date(str(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}'), alias, date)

        if (len(args) > 1):
            date_to = ''
            try:
                date_to = datetime.strptime(args[1],'%d.%m.%Y')
            except ValueError:
                await ctx.send("Invalid format in date 2 - should be 01.12.2021")
                return

            if ("ukesgolf" in ctx.channel.name):
                members = Members(f'{ctx.guild.name}', 'Medlemmer.xlsx')
                members.parse()
                scorecards = get_scorecards_date(str(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}'), alias, date, date_to, members.member_list)
            else:
                scorecards = get_scorecards_date(str(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}'), alias, date, date_to)

        if (scorecards.scorecards):
            if ("ukesgolf" in ctx.channel.name):
                scorecards.sort_players_points()
                embed = scorecards.get_embed_league(ctx.bot.user.avatar.url)
            else:
                embed = scorecards.get_embed(ctx.author.avatar.url)

            if (embed != None):
                await ctx.send(embed=embed)
            else:
                print("Embed not OK")
                scorecards.save_scorecards_text(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}/scores.txt')
                await ctx.send('https://giphy.com/embed/32mC2kXYWCsg0')
                await ctx.send(f'WOW {ctx.author.mention}, thats a lot of scores!)')
        else:
            await ctx.send("No courses found")

    @commands.command(name='udiscleague', aliases=['uleague'], brief='[uDiscLeague-link]', description='Parse uDisc League link to a scorecard')
    async def ukesgolf(self, ctx, *args,):
        if len(args) == 0:
            await ctx.send('No league specified, see %help udiscleague')
            return

        udisc_league = LeagueScraper(args[0])
        scraper_list = [udisc_league]
        self.scrape(scraper_list)

        date = udisc_league.score_card.date_time.strftime('%Y-%m-%d%H%M')
        file_name = f'{date}-{udisc_league.score_card.coursename}-{udisc_league.score_card.layoutname}-Udisc.csv'
        scorecard_writer = ScorecardWriter(f'{os.getcwd()}/cfg/{ctx.guild.name}/{ctx.channel}', file_name)
        header, data = udisc_league.score_card.get_csv()
        scorecard_writer.write(header, data)


        embed = udisc_league.score_card.get_embed(ctx.author.avatar.url)
        if (embed != None):
            await ctx.send(embed=embed)
        else:
            ctx.send("Scorecard stored, but scores is to big to display!")
