import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.parse
import time

class DiscStock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discs = []

    class Disc:
        def __init__(self):
            self.name = ''
            self.manufacturer = ''
            self.price = ''
            self.store = ''
            self.link = ''

    @commands.command(brief='Search for disc', description='Search for disc in norwegian stores and list if in stock')
    async def disc(self, ctx, *args, sep=" "):
        self.discs = []
        if len(args) == 0:
            await ctx.send('No disc specified, see %help disc')
            return

        disc_search = sep.join(args)        

        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.page_load_strategy = 'eager'

        with webdriver.Chrome(options=chrome_options) as driver:
            url = urllib.parse.quote(f'https://www.discinstock.no/?name={disc_search}', safe='?:/=')
            driver.get(url)
            time.sleep(1)
            content = driver.page_source
            soup = BeautifulSoup(content, "html.parser")

            for a in soup.findAll("div", class_="col"):
                disc = self.Disc()
                disc.manufacturer = a.find("h6", class_="text-muted font-monospace h-100").getText()
                disc.name = a.find("span", class_="fs-5").getText()                
                disc.price = a.find("span", class_="flex-shrink-1 display-6 mt-1").getText()
                disc.store = a.find("span", class_="mx-auto text-muted").getText()
                link = a.find('a', href=True)
                disc.link = link['href']

                self.discs.append(disc)

        if(len(self.discs) == 0):
            await ctx.send("No discs found")
            return        
        elif(len(self.discs)) == 1:
            embed_title = f'Found {len(self.discs)} Disc!'            
        else:
            embed_title = f'Found {len(self.discs)} Discs!'
        embed = discord.Embed(title=embed_title, color=0xFF5733)

        for disc in self.discs:            
            embed.add_field(name=disc.name, value=f'{disc.manufacturer}\nPrice: {disc.price}\n[{disc.store}]({disc.link})')

        await ctx.send(embed=embed)
