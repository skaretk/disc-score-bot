import os
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime
import nextcord
from nextcord.ext import commands, application_checks
from nextcord import Interaction, SlashOption
import dateutil.parser as dparser
from scrapers.udisc import LeagueScraper
import utilities
import validators
from .files.udisccsvreader import UdiscCsvReader
from .files.scorecardwriter import ScorecardWriter
from .alias import Alias
from .competition import Competition

class Scores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def scrape(self, scraper_list):
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=len(scraper_list)) as executor:
            for scraper in scraper_list:
                future = executor.submit(scraper.scrape)

        print(f'Spent {round(time.time() - start_time, 2)} scraping')

    def get_scorecards(self, path, alias):
        '''Get all scorecards'''
        competition = Competition()
        for file in os.listdir(path):
            if file.endswith(".csv"):
                reader = UdiscCsvReader(path, file)
                scorecard = reader.parse()

                # Add aliases
                for player in scorecard.players:
                    competition.add_player_alias(player, alias)

                competition.add_scorecard(scorecard)

        return competition

    def get_scorecards_course(self, path, alias, course):
        '''Get all scorecards for a course'''
        competition = Competition()
        for file in os.listdir(path):
            if file.endswith(".csv"):
                reader = UdiscCsvReader(path, file)
                scorecard = reader.contain_course(course)

                if scorecard is not None and scorecard.course.name is not None:
                    if course.lower() in scorecard.course.name.lower():
                        # Add aliases
                        for player in scorecard.players:
                            competition.add_player_alias(player, alias)

                        competition.add_scorecard(scorecard)

        return competition

    def get_scorecards_date(self, path, alias, date:datetime, date_to:datetime):
        '''Get all scorecards within date(s)'''
        competition = Competition()
        for file in os.listdir(path):
            if file.endswith(".csv"):
                reader = UdiscCsvReader(path, file)
                scorecard = reader.contain_dates(date, date_to)

                if scorecard is not None:
                    # Add aliases
                    for player in scorecard.players:
                        competition.add_player_alias(player, alias)

                    competition.add_scorecard(scorecard)

        return competition

    # Checks
    def has_scorecards():
        '''Does the channel contain any scorecards'''
        async def predicate(interaction:Interaction):
            folder = Path(f'{os.getcwd()}/cfg/{interaction.guild.name}/{interaction.channel}')
            if utilities.is_path_empty(folder):
                await interaction.send("No scorecards found")
                return False
            return True
        return application_checks.check(predicate)

    # Slash commands
    @nextcord.slash_command(name="scores", description="Score commands", guild_ids=[603273004641681441])
    async def scores(self):
        pass

    @scores.subcommand(name="print", description="Print stored scores!")
    @has_scorecards()
    async def scores_print(
        self,
        interaction:Interaction
    ):
        alias = Alias(interaction.guild.name)
        alias.parse()

        path = Path(f'{os.getcwd()}/cfg/{interaction.guild.name}/{interaction.channel}')
        competition = self.get_scorecards(path, alias)

        if competition.scorecards:
            embed = competition.get_embed(interaction.user.avatar.url)

            if embed is not None:
                await interaction.send(embed=embed)
            else:
                print("Embed not OK")
                competition.save_scorecards_text(f'{path}/scores.txt')
                await interaction.send('https://giphy.com/embed/32mC2kXYWCsg0')
                await interaction.send(f'WOW {interaction.user.mention}, thats a lot of scores!)')
        else:
            await interaction.send("No courses found")

    @scores.subcommand(name='files', description='Lists stored files in this channel')
    @has_scorecards()
    async def scores_files(
        self,
        interaction:Interaction
    ):
        path = Path(f'{os.getcwd()}/cfg/{interaction.guild.name}/{interaction.channel}')
        scorecards = ''
        file_count = 0
        for file in os.listdir(path):
            if file.endswith(".csv"):
                file_count += 1
                print(os.path.join(f'{path}/{file}'))
                scorecards += f'\n{file}'

        msg_to_send = f'No of files: {file_count}\n{scorecards}'

        if len(msg_to_send) > 2000:
            await interaction.send(f'No of files: {file_count}')
        elif file_count:
            await interaction.send(msg_to_send)
        else:
            await interaction.send('No .csv files stored for this channel')

    @scores.subcommand(name='stats', description='Print statistics for scorecards')
    @has_scorecards()
    async def scores_stats(
        self,
        interaction:Interaction
    ):
        alias = Alias(interaction.guild.name)
        alias.parse()

        path = Path(f'{os.getcwd()}/cfg/{interaction.guild.name}/{interaction.channel}')
        competition = self.get_scorecards(path, alias)

        if competition.scorecards:
            embed = competition.get_stats_embed(interaction.user.avatar.url)
            await interaction.send(embed=embed)
        else:
            await interaction.send("No stats found")

    @scores.subcommand()
    async def dates(
        self,
        interaction:Interaction
    ):
        pass

    @dates.subcommand(name='list', description='Print dates for scorecards')
    @has_scorecards()
    async def scores_dates(
        self,
        interaction:Interaction
    ):
        date_list = []
        path = Path(f'{os.getcwd()}/cfg/{interaction.guild.name}/{interaction.channel}')
        for file in os.listdir(path):
            if file.endswith(".csv"):
                reader = UdiscCsvReader(path, file)
                scorecard = reader.parse()

                date = scorecard.date_time.date().strftime("%d.%m.%Y")
                if date not in date_list:
                    date_list.append(date)

        msg = "\n".join(date_list)

        await interaction.send(msg)

    @dates.subcommand(name='search', description='Search for scorecards within date(s)')
    @has_scorecards()
    async def scores_dates_search (
        self,
        interaction:Interaction,
        arg1:str=SlashOption(name="date", description="Date / Date from", required=True),
        arg2:str=SlashOption(name="date_to", description="Date To", required=False)
    ):
        if arg1 is None and arg2 is None:
            await interaction.send("Missing date(s)")
            return

        alias = Alias(interaction.guild.name)
        alias.parse()

        path = Path(f'{os.getcwd()}/cfg/{interaction.guild.name}/{interaction.channel}')

        if arg1 is not None:
            try:
                date = dparser.parse(arg1, dayfirst=True, fuzzy=True)
            except dparser.ParserError:
                date = datetime.date.today()

            if arg2 is not None:
                try:
                    date_to = dparser.parse(arg2, dayfirst=True, fuzzy=True)
                except dparser.ParserError:
                    date_to = datetime.date.today()
            else:
                date_to = None
            competition = self.get_scorecards_date(path, alias, date, date_to)

        if competition.scorecards:
            embed = competition.get_embed(interaction.user.avatar.url)

            if embed is not None:
                await interaction.send(embed=embed)
            else:
                print("Embed not OK")
                competition.save_scorecards_text(f'{path}/scores.txt')
                await interaction.send('https://giphy.com/embed/32mC2kXYWCsg0')
                await interaction.send(f'WOW {interaction.user.mention}, thats a lot of scores!)')
        else:
            await interaction.send("No scores found")

    @scores.subcommand()
    async def courses(self, interaction:Interaction):
        pass

    @courses.subcommand(name='print', description='Print stored courses')
    @has_scorecards()
    async def courses_print(
        self,
        interaction:Interaction
    ):
        course_list = []
        path = Path(f'{os.getcwd()}/cfg/{interaction.guild.name}/{interaction.channel}')
        for file in os.listdir(path):
            if file.endswith(".csv"):
                reader = UdiscCsvReader(path, file)
                scorecard = reader.parse()

                if scorecard.course.name is not None and scorecard.course.name not in course_list:
                    course_list.append(scorecard.course.name)

        if len(course_list) != 0:
            msg = "\n".join(course_list)
        else:
            msg = "Could not find any stored courses"

        await interaction.send(msg)

    @courses.subcommand(name="search", description='Search and print scorecards for course')
    @has_scorecards()
    async def courses_search(
        self,
        interaction:Interaction,
        course:str=SlashOption(name="course", description="Course to search for", required=True)
    ):
        alias = Alias(interaction.guild.name)
        alias.parse()

        path = Path(f'{os.getcwd()}/cfg/{interaction.guild.name}/{interaction.channel}')
        competition = self.get_scorecards_course(path, alias, course)
        embed = competition.get_embed(interaction.user.avatar.url)

        if embed is not None:
            await interaction.send(embed=embed)
        else:
            await interaction.send("No courses found!")

    @scores.subcommand(name="udiscleague", description="Parse uDisc League")
    async def udiscleague(
        self,
        interaction:Interaction,
        url:str=SlashOption(name="url", description="Link to parse", required=True)
    ):
        if not validators.url(url) or "udisc.com" not in url.lower():
            await interaction.send("Not an valid url")
            return

        await interaction.response.defer()
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for scores online"))

        league = LeagueScraper(url)
        scraper_list = [league]
        self.scrape(scraper_list)

        date = league.scorecard.date_time.strftime('%Y-%m-%d')
        file_name = f'{league.scorecard.name.replace(" ", "-")}_{date}.csv'
        scorecard_writer = ScorecardWriter(f'{os.getcwd()}/cfg/{interaction.guild.name}/{interaction.channel}', file_name)
        header, data = league.scorecard.get_csv()
        scorecard_writer.write(header, data)

        embed = league.scorecard.get_embed(interaction.user.avatar.url)
        if embed is not None:
            await interaction.send(embed=embed)
        else:
            interaction.send("Scorecard stored, but scores is to big to display!")

        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
