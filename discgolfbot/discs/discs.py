from concurrent.futures import ThreadPoolExecutor
from discord_utils.embed_validation import validate_embed
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from scrapers.discScrapers import DiscScrapers
from scrapers.marshallstreet import DiscFlightScraper
from .store import Store, split_discs_in_stores

import time
from typing import Optional

class Discs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discs = []
        self.stores = []

    def scrape(self, scraper_list):
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=len(scraper_list)) as executor:
            for disc_scraper in scraper_list:
                future = executor.submit(disc_scraper.scrape)

        print(f'Spent {round(time.time() - start_time, 2)} scraping')

        for disc_scraper in scraper_list:
            self.discs.extend(disc_scraper.discs)

    def get_disc_image(self, embed:nextcord.Embed):
        for disc in self.discs:
            # Set image
            if disc.img:
                if disc.img.lower().endswith(('.png', '.jpg', '.jpeg')):
                    embed.set_thumbnail(url=(disc.img))
                    return True
        return False

    def format_discs_description(self):
        description_text = ''
        for store in self.stores:
            store_string_value = ""
            for disc in store.discs:
                # First disc
                if disc == store.discs[0]:
                    if description_text:
                        store_string_value += f'\n'
                    store_string_value += f'**{store.store}**\n[{disc.name}]({disc.url}) {disc.price}'
                # append
                else:
                    store_string_value += f'\n[{disc.name}]({disc.url}) {disc.price}'
                # Print if last disc
                if disc == store.discs[-1]:
                    description_text += store_string_value

        return description_text

    def get_embed_discs(self):
        if len(self.discs) == 0:
            return None

        embed_title = f'Found {len(self.discs)} {"Disc!" if len(self.discs) == 1 else "Discs!"}'
        embed = nextcord.Embed(title=embed_title, color=0x004899)

        # Split discs into store lists
        self.stores = split_discs_in_stores(self.discs)
        # Format output
        embed.description = self.format_discs_description()
        # Validate and return embed
        if validate_embed(embed) == True:
            return embed
        else:
            return None

    def get_embed_disc_flight(self, disc_flight_scraper):
        if (len(self.discs) == 1):
            disc = self.discs[0]
            if (disc.manufacturer == "Other"):
                embed = nextcord.Embed(title=f'{disc.name}', color=0x004899)
            else:
                embed = nextcord.Embed(title=f'{disc.manufacturer} {disc.name}', color=0x004899)
            embed.add_field(name='Flight', value=f'{disc.speed} {disc.glide} {disc.turn} {disc.fade}', inline=True)
            embed.set_image(url=disc.flight_url)
            embed.set_footer(text="Marshall Street", icon_url=disc_flight_scraper.icon_url)

            # Validate and return embed
            if (validate_embed(embed) == True):
                return embed
            else:
                return None
        else:
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
            self.discs = []
            disc_scrapers = DiscScrapers(search_item)
            self.scrape(disc_scrapers.norwegian_scrapers)

            embed = self.get_embed_discs()
            if embed is not None:
                if self.get_disc_image(embed) == False:
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
            self.discs = []
            disc_scrapers = DiscScrapers(search_item)
            self.scrape(disc_scrapers.voec_scrapers)

            embed = self.get_embed_discs()
            if embed is not None:
                if self.get_disc_image(embed) == False:
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
            self.discs = []
            disc_scrapers = DiscScrapers(search_item)
            self.scrape(disc_scrapers.all_scrapers)

            embed = self.get_embed_discs()
            if embed is not None:
                if self.get_disc_image(embed) == False:
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
        self.discs = []
        if len(args) == 0:
            await ctx.send(f'No disc specified {ctx.message.author.mention}, see %help disc_flight')
            return

        search = sep.join(args)
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for discs online"))

        start_time = time.time()
        scraper_list = [DiscFlightScraper(search)]
        self.scrape(scraper_list)

        embed = self.get_embed_disc_flight(scraper_list[0])
        if embed is not None:
            await ctx.send(ctx.author.mention, embed=embed)
        else:
            await ctx.send(f'Could not find flight path for {search} {ctx.author.mention}')

        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
        print(f'TOTAL {round(time.time() - start_time, 2)} scraping for disc flightpath')

    # Slash commands
    @nextcord.slash_command(name="disc", description="Discs commands", guild_ids=[])
    async def disc_slash_command(self):
        pass

    @disc_slash_command.subcommand(name="search", description="Search for discs in stores!")
    async def disc_search_slash_command(
        self,
        interaction: Interaction,
        search: str = SlashOption(name="disc", description="Disc to search for", required=True),
        where: Optional[int] = SlashOption(name="where", description="Where to search", choices={"Norway": 1, "VOEC": 2, "World": 3}, required=False)
    ):
        await interaction.response.defer()
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for discs online"))

        start_time = time.time()
        self.discs = []
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
        embed = self.get_embed_discs()
        if embed is not None:
            if self.get_disc_image(embed) == False:
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
        self.discs = []
        await interaction.response.defer()
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for discs online"))

        start_time = time.time()
        scraper_list = [DiscFlightScraper(search)]
        self.scrape(scraper_list)

        embed = self.get_embed_disc_flight(scraper_list[0])
        if embed is not None:
            await interaction.followup.send(interaction.user.mention, embed=embed)
        else:
            await interaction.followup.send(f'Could not find flight path for {search} {interaction.user.mention}')

        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
        print(f'TOTAL {round(time.time() - start_time, 2)} scraping for disc flightpath')
