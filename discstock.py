import time
import threading
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
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for discs online"))
        start_time = time.time()
        scraper_list = list()

        disc_in_stock_scraper = scraper.DiscInStock(disc_search)
        frisbeefeber_scraper = scraper.FrisbeeFeber(disc_search)
        sunesport_scraper = scraper.SuneSport(disc_search)
        discconnetion_scraper = scraper.Discconnection(disc_search)
        discexpress_scraper = scraper.DiscExpress(disc_search)
        latitude64_scraper = scraper.Latitude64(disc_search)
  
        thread1 = threading.Thread(target=disc_in_stock_scraper.scrape)
        thread1.start()
        scraper_list.append(thread1)
        thread2 = threading.Thread(target=frisbeefeber_scraper.scrape)
        thread2.start()
        scraper_list.append(thread2)
        thread3 = threading.Thread(target=sunesport_scraper.scrape)
        thread3.start()
        scraper_list.append(thread3)
        thread4 = threading.Thread(target=discconnetion_scraper.scrape)
        thread4.start()
        scraper_list.append(thread4)
        thread5 = threading.Thread(target=discexpress_scraper.scrape)
        thread5.start()
        scraper_list.append(thread5)
        thread6 = threading.Thread(target=latitude64_scraper.scrape)
        thread6.start()
        scraper_list.append(thread6)
        
        # Wait for all threads to complete
        for thread in scraper_list:
            thread.join()

        end_time = time.time()
        print(f'Spent {end_time - start_time} scraping')

        self.discs.extend(disc_in_stock_scraper.discs)
        self.discs.extend(frisbeefeber_scraper.discs)
        self.discs.extend(sunesport_scraper.discs)
        self.discs.extend(discconnetion_scraper.discs)
        self.discs.extend(discexpress_scraper.discs)
        self.discs.extend(latitude64_scraper.discs)

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
