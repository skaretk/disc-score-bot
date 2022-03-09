import nextcord
from nextcord.ext import commands
import time
from concurrent.futures import ThreadPoolExecutor
from scrapers.discScrapers import DiscScrapers
from scrapers.marshallstreet import DiscFlightScraper
from discord_utils.embed_validation import validate_embed

class Discs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discs = []

    def scrape(self, scraper_list):    
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=len(scraper_list)) as executor:
            for disc_scraper in scraper_list:
                future = executor.submit(disc_scraper.scrape)
        
        print(f'Spent {round(time.time() - start_time, 2)} scraping')

        for disc_scraper in scraper_list:
            self.discs.extend(disc_scraper.discs)

    async def print_discs(self, ctx, search_item):
        if(len(self.discs) == 0):
            await ctx.send(f'{ctx.author.mention} - **{search_item}**, No discs in stock')
            return        
        elif(len(self.discs)) == 1:
            embed_title = f'Found {len(self.discs)} Disc!'            
        else:
            embed_title = f'Found {len(self.discs)} Discs!'
        embed = nextcord.Embed(title=embed_title, color=0x004899)

        img_set = False
        for disc in self.discs:            
            embed.add_field(name=disc.name, value=f'{disc.manufacturer}\nPrice: {disc.price}\n[{disc.store}]({disc.url})')
            if (disc.img and img_set == False):
                if (disc.img.lower().endswith(('.png', '.jpg', '.jpeg'))):
                    embed.set_thumbnail(url=(disc.img))
                    img_set = True
        
        if (img_set == False):
            embed.set_thumbnail(url=(ctx.author.avatar.url))
        
        # Validate and send Embed
        if (validate_embed(embed) == True):
            await ctx.send(f'{ctx.author.mention} - **{search_item}**', embed=embed)
        else:
            await ctx.send(f'{ctx.author.mention}, WOW thats a lot of **{search_item}** discs! ({len(self.discs)}!)')
            await ctx.send("https://giphy.com/embed/32mC2kXYWCsg0")

    @commands.command(aliases=['d'], brief='%disc [disc1, disc2, etc]', description='Search for disc in norwegian and VOEC approved sites')
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
            scrapers = DiscScrapers(search_item)
            scraper_list = []
            scraper_list.extend(scrapers.norwegian)
            scraper_list.extend(scrapers.voec)

            self.scrape(scraper_list)
            await self.print_discs(ctx, search_item)
        
        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
        print(f'TOTAL {round(time.time() - start_time, 2)} scraping')

    @commands.command(name='disc_all', aliases=['d_a'], brief='List discs from all scrapers', description='Lists all discs in store for all sites added')
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
            scrapers = DiscScrapers(search_item)
            scraper_list = []
            scraper_list.extend(scrapers.norwegian)
            scraper_list.extend(scrapers.voec)
            scraper_list.extend(scrapers.international)

            self.scrape(scraper_list)
            await self.print_discs(ctx, search_item)
        
        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
        print(f'TOTAL {round(time.time() - start_time, 2)} scraping')

    @commands.command(name='disc_flight', aliases=['d_f'], brief='Disc flightpath', description='Gets the flightpath of the specified disc')
    async def disc_flight(self, ctx, *args, sep=" "):
        self.discs = []
        if len(args) == 0:
            await ctx.send(f'No disc specified {ctx.message.author.mention}, see %help disc_flight')
            return

        search = sep.join(args)
        await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for discs online"))        
        
        scraper_list = [DiscFlightScraper(search)]
        self.scrape(scraper_list)

        if (len(self.discs) == 1):
            disc = self.discs[0]
            if (disc.manufacturer == "Other"):
                embed = nextcord.Embed(title=f'{disc.name}', color=0x004899)
            else:
                embed = nextcord.Embed(title=f'{disc.manufacturer} {disc.name}', color=0x004899)
            embed.add_field(name='Flight', value=f'{disc.speed} {disc.glide} {disc.turn} {disc.fade}', inline=True)
            embed.set_image(url=disc.flight_url)
            embed.set_footer(text="Provided by Marshall Street", icon_url=scraper_list[0].icon_url)
            
            # Validate and send Embed
            if (validate_embed(embed) == True):
                await ctx.send(ctx.author.mention, embed=embed)
            else:
                await ctx.send(f'{ctx.author.mention}, Could not show the disc flight for {search}!)')
                await ctx.send("https://giphy.com/embed/32mC2kXYWCsg0")
        else:
            await ctx.send(f'Could not find flight path for {search} {ctx.author.mention}')
        
        await self.bot.change_presence(activity=nextcord.Game(name="Disc golf"))
