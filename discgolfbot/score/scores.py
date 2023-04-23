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

# Application checks
def has_scorecards():
    """Does the channel contain any scorecards"""
    async def predicate(interaction:Interaction):
        folder = Path.cwd() / "cfg" / interaction.guild.name / interaction.channel.name
        if utilities.is_path_empty(folder):
            await interaction.send("No scorecards found")
            return False
        return True
    return application_checks.check(predicate)

class Scores(commands.Cog):
    """Scores Class, Fetches scorecards locally or over web"""
    def __init__(self, bot):
        self.bot = bot

    def scrape(self, scraper_list):
        """Scrape for scorecards over web"""
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=len(scraper_list)) as executor:
            for scraper in scraper_list:
                future = executor.submit(scraper.scrape)

        print(f'Spent {round(time.time() - start_time, 2)} scraping')

    def folder_path(self, interaction:Interaction):
        """Returns the folder to the guild and channel"""
        return Path.cwd() / "cfg" / interaction.guild.name / interaction.channel.name

    @commands.Cog.listener()
    async def on_message(self, message):
        """Listenes for attachement in a discord channel, stores it and displays the scorecard"""
        if message.attachments:
            for attachment in message.attachments:
                if 'text/csv' in attachment.content_type:
                    folder = Path.cwd() / "cfg" / message.guild.name / message.channel.name
                    if not folder.exists():
                        folder.mkdir()
                    file = folder / attachment.filename
                    await attachment.save(fp=file) # saves the file in a guild/channel folder
                    print(f'csv attached and stored in {file}!')

                    reader = UdiscCsvReader(file)
                    scorecard = reader.parse()

                    if scorecard is None:
                        await message.channel.send("Stored scorecard, could not parse it!")
                    else:
                        embed = scorecard.get_embed(message.author.avatar.url)
                        if embed is not None:
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send("Stored scorecard, but it is to big to display!")

                    await message.delete()

    # Slash commands
    @nextcord.slash_command(name="scores", description="Score commands", guild_ids=[])
    async def scores(self):
        """/scores"""

    @scores.subcommand(name="print", description="Print stored scores!")
    @has_scorecards()
    async def scores_print(
        self,
        interaction:Interaction
    ):
        """/scores print"""
        folder = self.folder_path(interaction)
        competition = Competition.parse(folder, Alias(interaction.guild.name))

        if competition.scorecards:
            embed = competition.get_embed(interaction.user.avatar.url)

            if embed is not None:
                await interaction.send(embed=embed)
            else:
                print("Embed not OK")
                competition.save_scorecards_text(folder / "scores.txt")
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
        """/scores files"""
        folder = self.folder_path(interaction)
        scorecards = ''
        file_count = 0
        for file in list(folder.iterdir()):
            if file.suffix == ".csv":
                file_count += 1
                print(folder / file)
                scorecards += f'\n{file.name}'

        msg = f'No of files: {file_count}\n{scorecards}'

        if len(msg) > 2000:
            await interaction.send(f'No of files: {file_count}')
        elif file_count:
            await interaction.send(msg)
        else:
            await interaction.send('No .csv files stored for this channel')

    @scores.subcommand(name='stats', description='Print statistics for scorecards')
    @has_scorecards()
    async def scores_stats(
        self,
        interaction:Interaction
    ):
        """/scores stats"""
        folder = self.folder_path(interaction)
        competition = Competition.parse(folder, Alias(interaction.guild.name))

        if competition.scorecards:
            embed = competition.get_stats_embed(interaction.user.avatar.url)
            await interaction.send(embed=embed)
        else:
            await interaction.send("No stats found")

    @scores.subcommand()
    async def dates(self, interaction:Interaction):
        """/scores dates"""

    @dates.subcommand(name='list', description='Print dates for scorecards')
    @has_scorecards()
    async def scores_dates(
        self,
        interaction:Interaction
    ):
        """/scores dates list"""
        date_list = []
        folder = self.folder_path(interaction)
        for file in list(folder.iterdir()):
            if file.suffix == ".csv":
                reader = UdiscCsvReader(file)
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
        """/scores dates search [date] [date_to]"""
        if arg1 is None and arg2 is None:
            await interaction.send("Missing date(s)")
            return

        folder = self.folder_path(interaction)

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
            competition = Competition.parse_dates(folder, Alias(interaction.guild.name), date, date_to)

        if competition.scorecards:
            embed = competition.get_embed(interaction.user.avatar.url)

            if embed is not None:
                await interaction.send(embed=embed)
            else:
                print("Embed not OK")
                competition.save_scorecards_text(f'{folder}/scores.txt')
                await interaction.send('https://giphy.com/embed/32mC2kXYWCsg0')
                await interaction.send(f'WOW {interaction.user.mention}, thats a lot of scores!)')
        else:
            await interaction.send("No scores found")

    @scores.subcommand()
    async def courses(self, interaction:Interaction):
        """/scores courses"""

    @courses.subcommand(name='print', description='Print stored courses')
    @has_scorecards()
    async def courses_print(
        self,
        interaction:Interaction
    ):
        """/scores courses print"""
        course_list = []
        folder = self.folder_path(interaction)
        for file in list(folder.iterdir()):
            if file.suffix == ".csv":
                reader = UdiscCsvReader(file)
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
        """/scores courses search [course]"""
        folder = self.folder_path(interaction)
        competition = Competition.parse_course(folder, Alias(interaction.guild.name), course)
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
        """/udiscleague [url]"""
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
        folder = self.folder_path(interaction)
        scorecard_writer = ScorecardWriter(folder, file_name)
        header, data = league.scorecard.get_csv()
        scorecard_writer.write(header, data)

        embed = league.scorecard.get_embed(interaction.user.avatar.url)
        if embed is not None:
            await interaction.send(embed=embed)
        else:
            interaction.send("Scorecard stored, but scores is to big to display!")

        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
