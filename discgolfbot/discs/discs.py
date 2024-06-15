from concurrent.futures import ThreadPoolExecutor
import time
from typing import Optional

from discord_utils.embed_validation import validate_embed
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from scrapers.discScrapers import DiscScrapers, DiscNewsScrapers
from scrapers.marshallstreet import DiscFlightScraper
from apis.discitapi import DiscitApi
from .store import split_discs_in_stores

class Discs(commands.Cog):
    """Discs cog"""
    def __init__(self, bot):
        self.bot = bot
        self.discs = []
        self.stores = []

    def scrape(self, scraper_list):
        """Scrape discs from disc scraper_list"""
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=len(scraper_list)) as executor:
            for disc_scraper in scraper_list:
                future = executor.submit(disc_scraper.scrape)

        print(f'Spent {round(time.time() - start_time, 2)} scraping')

        for disc_scraper in scraper_list:
            self.discs.extend(disc_scraper.discs)

    def get_disc_image(self, embed:nextcord.Embed):
        """Fetch the image from the first disc in the list"""
        for disc in self.discs:
            # Set image
            if disc.img:
                if disc.img.lower().endswith(('.png', '.jpg', '.jpeg')):
                    embed.set_thumbnail(url=(disc.img))
                    return True
        return False

    def format_discs_description(self):
        """Format the discs with stores"""
        text = ''
        for store in self.stores:
            text += f'**{store.store}**' if store == self.stores[0] else f'\n**{store.store}**'
            for disc in store.discs:
                text += f'\n[{disc.name}]({disc.url}) {disc.price}'

        return text

    def get_discs_embed(self):
        """Return discs embed"""
        if len(self.discs) == 0:
            return None

        no_discs = 0
        for store in self.stores:
            no_discs += len(store.discs)

        embed_title = f'Found {no_discs} {"Disc!" if no_discs == 1 else "Discs!"}'
        embed = nextcord.Embed(title=embed_title, color=0x004899)

        # Format output
        embed.description = self.format_discs_description()
        # Validate and return embed
        if validate_embed(embed):
            return embed
        return None

    def get_disc_flight_embed(self, disc_flight_scraper):
        """Return disc flight embed"""
        if len(self.discs) == 1:
            disc = self.discs[0]
            if disc.manufacturer == "Other":
                embed = nextcord.Embed(title=f'{disc.name}', color=0x004899)
            else:
                embed = nextcord.Embed(title=f'{disc.manufacturer} {disc.name}', color=0x004899)
            embed.add_field(name='Flight', value=f'{disc.flight}', inline=True)
            embed.set_image(url=disc.url)
            embed.set_footer(text="Marshall Street", icon_url=disc_flight_scraper.icon_url)

            # Validate and return embed
            if validate_embed(embed):
                return embed
        return None

    def get_disc_lookup_embed(self):
        """Return disc lookup embed"""
        if len(self.discs) == 1:
            disc = self.discs[0]
            embed = nextcord.Embed(title=f'{disc.manufacturer} {disc.name}',
                                   description=f'**{disc.flight}**',
                                   color=int(disc.color.lstrip('#'), 16))
            embed.set_image(url=disc.img)
        elif len(self.discs) >= 1:
            disc_text = ''
            for disc in self.discs:
                disc_text += f'* {disc.name} {disc.flight}'
                if disc != self.discs[-1]:
                    disc_text += '\n'
            embed = nextcord.Embed(title=f'Found {len(self.discs)} discs',
                                   description=f'{disc_text}',
                                   color=0x004899)
        else:
            return None

        embed.set_footer(text="DiscIt")

        # Validate and return embed
        if validate_embed(embed):
            return embed

        return None

    @commands.command(aliases=['Disc', 'disk', 'Disk', 'd'], brief='%disc disc1, disc2, etc', description='Search for disc in norwegian sites')
    async def disc(self, ctx, *args, sep=" "):
        if len(args) == 0:
            await ctx.send('No disc specified, see %help disc')
            return

        search = sep.join(args)
        search_list = search.split(", ")
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for discs online"))

        start_time = time.time()

        for search_item in search_list:
            self.discs.clear()
            disc_scrapers = DiscScrapers(search_item)
            self.scrape(disc_scrapers.norwegian_scrapers)
            self.stores = split_discs_in_stores(self.discs)

            embed = self.get_discs_embed()
            if embed is not None:
                if self.get_disc_image(embed) is False:
                    embed.set_thumbnail(url=(ctx.author.avatar.url))
                await ctx.send(f'{ctx.author.mention} - **{search_item}**', embed=embed)
            else:
                if len(self.discs) == 0:
                    await ctx.send(f'{ctx.author.mention} - **{search_item}**, No discs in stock')
                else:
                    await ctx.send(f'{ctx.author.mention}, WOW thats a lot of **{search_item}** discs! ({len(self.discs)}!)\nTIP: Include plastic type to reduce number of results')
                    await ctx.send("https://giphy.com/embed/32mC2kXYWCsg0")

        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
        print(f'TOTAL {round(time.time() - start_time, 2)} scraping')

    @commands.command(aliases=['Disc_voec', 'disk_voec', 'Disk_voec'], brief='%disc_voec disc1, disc2, etc', description='Search for disc in norwegian and VOEC approved sites')
    async def disc_voec(self, ctx, *args, sep=" "):
        if len(args) == 0:
            await ctx.send('No disc specified, see %help disc_voec')
            return

        search = sep.join(args)
        search_list = search.split(", ")
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for discs online"))

        start_time = time.time()

        for search_item in search_list:
            self.discs.clear()
            disc_scrapers = DiscScrapers(search_item)
            self.scrape(disc_scrapers.voec_scrapers)
            self.stores = split_discs_in_stores(self.discs)

            embed = self.get_discs_embed()
            if embed is not None:
                if self.get_disc_image(embed) is False:
                    embed.set_thumbnail(url=(ctx.author.avatar.url))
                await ctx.send(f'{ctx.author.mention} - **{search_item}**', embed=embed)
            else:
                if len(self.discs) == 0:
                    await ctx.send(f'{ctx.author.mention} - **{search_item}**, No discs in stock')
                else:
                    await ctx.send(f'{ctx.author.mention}, WOW thats a lot of **{search_item}** discs! ({len(self.discs)}!)\nTIP: Include plastic type to reduce number of results')
                    await ctx.send("https://giphy.com/embed/32mC2kXYWCsg0")

        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
        print(f'TOTAL {round(time.time() - start_time, 2)} scraping')

    @commands.command(aliases=['disk_all', 'd_a'], brief='%disc_all disc1, disc2, etc', description='Lists all discs in store for all sites added')
    async def disc_all(self, ctx, *args, sep=" "):
        if len(args) == 0:
            await ctx.send('No disc specified, see %help disc_all')
            return

        search = sep.join(args)
        search_list = search.split(", ")
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for discs online"))

        start_time = time.time()

        for search_item in search_list:
            self.discs.clear()
            disc_scrapers = DiscScrapers(search_item)
            self.scrape(disc_scrapers.all_scrapers)
            self.stores = split_discs_in_stores(self.discs)

            embed = self.get_discs_embed()
            if embed is not None:
                if self.get_disc_image(embed) is False:
                    embed.set_thumbnail(url=(ctx.author.avatar.url))
                await ctx.send(f'{ctx.author.mention} - **{search_item}**', embed=embed)
            else:
                if len(self.discs) == 0:
                    await ctx.send(f'{ctx.author.mention} - **{search_item}**, No discs in stock')
                else:
                    await ctx.send(f'{ctx.author.mention}, WOW thats a lot of **{search_item}** discs! ({len(self.discs)}!)\nTIP: Include plastic type to reduce number of results')
                    await ctx.send("https://giphy.com/embed/32mC2kXYWCsg0")

        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
        print(f'TOTAL {round(time.time() - start_time, 2)} scraping')

    @commands.command(aliases=['Disc_flight', 'disk_flight', 'Disk_flight'], brief='%disc_flight disc', description='Get the flightpath of the given disc')
    async def disc_flight(self, ctx, *args, sep=" "):
        self.discs.clear()
        if len(args) == 0:
            await ctx.send(f'No disc specified {ctx.message.author.mention}, see %help disc_flight')
            return

        search = sep.join(args)
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for discs online"))

        start_time = time.time()
        scraper_list = [DiscFlightScraper(search)]
        self.scrape(scraper_list)

        embed = self.get_disc_flight_embed(scraper_list[0])
        if embed is not None:
            await ctx.send(ctx.author.mention, embed=embed)
        else:
            await ctx.send(f'Could not find flight path for {search} {ctx.author.mention}')

        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
        print(f'TOTAL {round(time.time() - start_time, 2)} scraping for disc flightpath')

    # Slash commands
    @nextcord.slash_command(name="disc", description="Discs commands", guild_ids=[])
    async def disc_slash_command(self, interaction: nextcord.Interaction):
        """/disc slash command. Main command"""
        pass

    @disc_slash_command.subcommand(name="search", description="Search for discs in stores!")
    async def disc_search_slash_command(
        self,
        interaction: Interaction,
        search: str = SlashOption(name="disc", description="Disc to search for", required=True),
        where: Optional[int] = SlashOption(name="where", description="Where to search", choices={"Norway": 1, "VOEC": 2, "World": 3}, required=False)
    ):
        """/disc search subcommand"""
        await interaction.response.defer()
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for discs online"))

        start_time = time.time()
        self.discs.clear()
        disc_scrapers = DiscScrapers(search)
        scraper_list = []
        if where is not None:
            if where == 1:
                scraper_list = disc_scrapers.norwegian_scrapers
            elif where == 2:
                scraper_list = disc_scrapers.voec_scrapers
            elif where == 3:
                scraper_list = disc_scrapers.all_scrapers
        else:
            scraper_list = disc_scrapers.norwegian_scrapers

        self.scrape(scraper_list)
        self.stores = split_discs_in_stores(self.discs)
        embed = self.get_discs_embed()
        if embed is not None:
            if self.get_disc_image(embed) is False:
                embed.set_thumbnail(url=(interaction.user.display_avatar))
            await interaction.followup.send(f'{interaction.user.mention} - **{search}**', embed=embed)
        else:
            if len(self.discs) == 0:
                await interaction.followup.send(f'{interaction.user.mention} - **{search}**, No discs in stock')
            else:
                await interaction.followup.send(f'{interaction.user.mention}, WOW thats a lot of **{search}** discs! ({len(self.discs)}!)\nTIP: Include plastic type to reduce number of results https://giphy.com/embed/32mC2kXYWCsg0')

        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
        print(f'TOTAL {round(time.time() - start_time, 2)} scraping')

    @disc_slash_command.subcommand(name="flight", description="Search for disc flight-path")
    async def disc_flight_slash_command(
        self,
        interaction: Interaction,
        search: str = SlashOption(name="disc", description="Disc to search for", required=True)
    ):
        """/disc flight subcommand"""
        self.discs.clear()
        await interaction.response.defer()
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for discs online"))

        start_time = time.time()
        scraper_list = [DiscFlightScraper(search)]
        self.scrape(scraper_list)

        embed = self.get_disc_flight_embed(scraper_list[0])
        if embed is not None:
            await interaction.followup.send(interaction.user.mention, embed=embed)
        else:
            await interaction.followup.send(f'Could not find flight path for {search} {interaction.user.mention}')

        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
        print(f'TOTAL {round(time.time() - start_time, 2)} scraping for disc flightpath')

    @disc_slash_command.subcommand(name="lookup", description="Search for discs with specific characteristics")
    async def disc_lookup_slash_command(
        self,
        interaction: Interaction,
        name: str = SlashOption(
            name="name",
            description="Disc name",
            required=False),
        brand: str = SlashOption(
            name="brand",
            description="Disc brand",
            required=False),
        category: str = SlashOption(
            name="category",
            description="Disc category",
            choices={"Distance Driver": "Distance Driver", "Hybrid Driver": "Hybrid Driver", "Control Driver": "Control Driver", "Midrange": "Midrange", "Putter": "Putter"},
            required=False),
        speed: str = SlashOption(
            name="speed",
            description="Disc speed",
            required=False),
        glide: str = SlashOption(
            name="glide",
            description="Disc glide",
            required=False),
        turn: str = SlashOption(
            name="turn",
            description="Disc turn",
            required=False),
        fade: str = SlashOption(
            name="fade",
            description="Disc fade",
            required=False),
        stability: str = SlashOption(
            name="stability",
            description="Disc stability",
            choices={"Stable": "Stable", "Overstable": "Overstable", "Very Overstable": "Very Overstable", "Understable": "Understable", "Very Understable": "Very Understable"},
            required=False)
    ):
        """/disc lookup subcommand"""
        self.discs.clear()
        await interaction.response.defer()
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for discs online"))

        start_time = time.time()
        api = DiscitApi()
        self.discs = api.get_disc(name=name,brand=brand,category=category,speed=speed,glide=glide,turn=turn,fade=fade,stability=stability)

        # If disc name is provided, fetch only that disc if we have an exact match
        if name is not None and len(self.discs) > 1:
            disc_match = next((disc for disc in self.discs if disc.name.lower() == name.lower()), None)
            if disc_match is not None:
                self.discs = [disc_match]

        self.discs.sort(key=lambda x: (float(x.speed), float(x.glide), float(x.turn), float(x.fade)))

        embed = self.get_disc_lookup_embed()

        if embed is not None:
            await interaction.followup.send(interaction.user.mention, embed=embed)
        else:
            await interaction.followup.send(f'Could not lookup the the disc(s) {interaction.user.mention}')

        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
        print(f'Spent {round(time.time() - start_time, 2)} looking up the disc(s)')

    @disc_slash_command.subcommand(name="news", description="Search for last updated discs in stores!")
    async def disc_news_slash_command(
        self,
        interaction: Interaction,
        days: Optional[int] = SlashOption(name="days", description="How long since the discs were added", required=False),
        where: Optional[int] = SlashOption(name="where", description="Where to search", choices={"Norway": 1, "VOEC": 2, "World": 3}, required=False)
    ):
        """/disc news subcommand"""
        await interaction.response.defer()
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for new discs online"))

        start_time = time.time()
        self.discs.clear()
        if days is not None:
            disc_scrapers = DiscNewsScrapers(days)
        else:
            disc_scrapers = DiscNewsScrapers(7)
        scraper_list = []
        if where is not None:
            if where == 1:
                scraper_list = disc_scrapers.norwegian_scrapers
            elif where == 2:
                scraper_list = disc_scrapers.voec_scrapers
            elif where == 3:
                scraper_list = disc_scrapers.all_scrapers
        else:
            scraper_list = disc_scrapers.norwegian_scrapers

        self.scrape(scraper_list)
        self.stores = split_discs_in_stores(self.discs, 5)
        embed = self.get_discs_embed()
        if embed is not None:
            if self.get_disc_image(embed) is False:
                embed.set_thumbnail(url=(interaction.user.display_avatar))
            await interaction.followup.send(f'{interaction.user.mention} - **NEWS**', embed=embed)
        else:
            if len(self.discs) == 0:
                await interaction.followup.send(f'{interaction.user.mention} - **NEWS**, Failed to get lastest discs')
            else:
                await interaction.followup.send(f'{interaction.user.mention}, WOW thats a lot of **NEW** discs! ({len(self.discs)}!)\n https://giphy.com/embed/32mC2kXYWCsg0')

        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
        print(f'TOTAL {round(time.time() - start_time, 2)} scraping')
