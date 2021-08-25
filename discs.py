import time
from concurrent.futures import ThreadPoolExecutor
import discord
from discord.ext import commands
import scraper

class Discs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discs = []    

    @commands.command(aliases=['d'], brief='Search for disc (Norway & VOEC)', description='Search for disc in norwegian and VOEC approved sites')
    async def disc(self, ctx, *args, sep=" "):
        self.discs = []
        if len(args) == 0:
            await ctx.send('No disc specified, see %help disc search')
            return

        disc_search = sep.join(args)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for discs online"))        
        
        scrapers = scraper.Scrapers(disc_search)
        scraper_list = []
        scraper_list.extend(scrapers.norwegian)
        scraper_list.extend(scrapers.voec)
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=len(scraper_list)) as executor:
            for disc_scraper in scraper_list:
                future = executor.submit(disc_scraper.scrape)
        
        end_time = time.time()
        print(f'Spent {end_time - start_time} scraping')

        for disc_scraper in scraper_list:
            self.discs.extend(disc_scraper.discs)

        if(len(self.discs) == 0):
            await ctx.send(f'Found no discs in stock {ctx.author.mention}')
            return        
        elif(len(self.discs)) == 1:
            embed_title = f'Found {len(self.discs)} Disc!'            
        else:
            embed_title = f'Found {len(self.discs)} Discs!'
        embed = discord.Embed(title=embed_title, color=0xFF5733)

        for disc in self.discs:            
            embed.add_field(name=disc.name, value=f'{disc.manufacturer}\nPrice: {disc.price}\n[{disc.store}]({disc.url})')
        embed.set_thumbnail(url=(ctx.author.avatar_url))

        if (len(embed) < 6000): # Size limit for embeds
            await ctx.send(embed=embed)
        else:
            print(len(embed))
            await ctx.send('https://giphy.com/embed/32mC2kXYWCsg0')
            await ctx.send(f'WOW {ctx.author.mention}, thats a lot of {disc_search} discs! ({len(self.discs)}!) ')

        await self.bot.change_presence(activity=discord.Game(name="Disc golf"))       

    @commands.command(pass_context=True, name='disc_all', aliases=['d_a'], brief='List discs from all scrapers', description='Lists all discs in store for all sites added')
    async def disc_all(self, ctx, *args, sep=" "):
        self.discs = []
        if len(args) == 0:
            await ctx.send('No disc specified, see %help disc_all')
            return

        disc_search = sep.join(args)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for discs online"))        

        scrapers = scraper.Scrapers(disc_search)
        scraper_list = []
        scraper_list.extend(scrapers.norwegian)
        scraper_list.extend(scrapers.voec)
        scraper_list.extend(scrapers.international)
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=len(scraper_list)) as executor:
            for disc_scraper in scraper_list:
                future = executor.submit(disc_scraper.scrape)
        
        end_time = time.time()
        print(f'Spent {end_time - start_time} scraping')

        for disc_scraper in scraper_list:
            self.discs.extend(disc_scraper.discs) 

        if(len(self.discs) == 0):
            await ctx.send(f'Found no discs in stock {ctx.author.mention}')
            return        
        elif(len(self.discs)) == 1:
            embed_title = f'Found {len(self.discs)} Disc!'            
        else:
            embed_title = f'Found {len(self.discs)} Discs!'
        embed = discord.Embed(title=embed_title, color=0xFF5733)

        for disc in self.discs:            
            embed.add_field(name=disc.name, value=f'{disc.manufacturer}\nPrice: {disc.price}\n[{disc.store}]({disc.url})')
        embed.set_thumbnail(url=(ctx.author.avatar_url))

        if (len(embed) < 6000): # Size limit for embeds
            await ctx.send(embed=embed)
        else:
            print(len(embed))
            await ctx.send('https://giphy.com/embed/32mC2kXYWCsg0')
            await ctx.send(f'WOW {ctx.author.mention}, thats a lot of {disc_search} discs! ({len(self.discs)}!) ')

        await self.bot.change_presence(activity=discord.Game(name="Disc golf"))
