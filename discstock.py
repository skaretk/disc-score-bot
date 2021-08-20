import asyncio
import time
import discord
from discord.ext import commands
import scraper

class DiscStock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discs = []    

    @commands.command(brief='Search for disc', description='Search for disc in stores and list if in stock')
    async def disc(self, ctx, *args, sep=" "):
        self.discs = []
        if len(args) == 0:
            await ctx.send('No disc specified, see %help disc')
            return

        disc_search = sep.join(args)
        
        disc_in_stock_scraper = scraper.DiscInStock(disc_search)
        frisbeefeber_scraper = scraper.FrisbeeFeber(disc_search)
        discconnetion_scraper = scraper.Discconnection(disc_search)
        start_time = time.time()
        await asyncio.gather(
            disc_in_stock_scraper.scrape(),
            frisbeefeber_scraper.scrape(),
            discconnetion_scraper.scrape())
        end_time = time.time()
        print(f'Spent {end_time - start_time} scraping')

        self.discs.extend(disc_in_stock_scraper.discs)
        self.discs.extend(frisbeefeber_scraper.discs)
        self.discs.extend(discconnetion_scraper.discs)

        if(len(self.discs) == 0):
            await ctx.send(f'Found no discs {ctx.author.mention}')
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