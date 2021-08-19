import asyncio
import time
import urllib.parse
import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

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

    def get_chrome(self):
        # support to get response status and headers
        opt = webdriver.ChromeOptions()
        opt.add_argument("--headless")
        opt.add_argument("--disable-extensions")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--disable-xss-auditor")
        #opt.add_argument("--disable-web-security")
        #opt.add_argument("--allow-running-insecure-content")
        #opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-setuid-sandbox")
        opt.add_argument("--disable-webgl")
        opt.add_argument("--disable-popup-blocking")
        opt.page_load_strategy = 'eager'
        browser = webdriver.Chrome(options=opt)
        browser.implicitly_wait(10)
        browser.set_page_load_timeout(30)
        return browser 

    @commands.command(brief='Search for disc', description='Search for disc in norwegian stores and list if in stock')
    async def disc(self, ctx, *args, sep=" "):
        self.discs = []
        if len(args) == 0:
            await ctx.send('No disc specified, see %help disc')
            return

        disc_search = sep.join(args)        

        print(f"Starting search: {time.strftime('%X')}")
        await asyncio.gather(
            self.scrape_discinstock(disc_search),
            self.scrape_frisbeefeber(disc_search),
            self.scrape_discconnection(disc_search))
        print(f"Finished search {time.strftime('%X')}")

        if(len(self.discs) == 0):
            await ctx.send(f'Found no discs {ctx.author.mention}')
            return        
        elif(len(self.discs)) == 1:
            embed_title = f'Found {len(self.discs)} Disc!'            
        else:
            embed_title = f'Found {len(self.discs)} Discs!'
        embed = discord.Embed(title=embed_title, color=0xFF5733)

        for disc in self.discs:            
            embed.add_field(name=disc.name, value=f'{disc.manufacturer}\nPrice: {disc.price}\n[{disc.store}]({disc.link})')
        embed.set_thumbnail(url=(ctx.author.avatar_url))

        if (len(embed) < 6000): # Size limit for embeds
            await ctx.send(embed=embed)
        else:
            print(len(embed))
            await ctx.send('https://giphy.com/embed/32mC2kXYWCsg0')
            await ctx.send(f'WOW {ctx.author.mention}, thats a lot of discs! ({len(self.discs)}!) ')           

    async def scrape_discinstock(self, disc_search):
        with self.get_chrome() as driver:
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

    async def scrape_frisbeefeber(self, disc_search):
        with self.get_chrome() as driver:
            url = urllib.parse.quote(f'https://www.frisbeefeber.no/search_result?keywords={disc_search}', safe='?:/=&')
            driver.get(url)
            content = driver.page_source
            soup = BeautifulSoup(content, "html.parser")
            store = 'frisbeefeber.no'

            for product in soup.select('li[class*="product-box-id-"]'):
                # Is product in stock ?
                not_in_stock = product.find("div", class_="product not-in-stock-product")
                if (not_in_stock is not None):
                    continue
                disc = self.Disc()
                disc.name = product.find("a", class_="title col-md-12").getText()
                # Search engine gives false results, check if the disc name is correct
                if (disc_search.lower() not in disc.name.lower()):
                    continue
                div_manufacturer = product.find("div", class_="manufacturer-box")
                alt_manufacturer = div_manufacturer.find("img", alt=True)
                disc.manufacturer = alt_manufacturer['alt']
                disc.price = product.find("div", class_="price col-md-12").getText()
                disc.store = store
                link = product.find('a', href=True)
                disc.link = link['href']

                self.discs.append(disc)            

    async def scrape_discconnection(self, disc_search):
        with self.get_chrome() as driver:
            url = urllib.parse.quote(f'https://discconnection.dk/default.asp?page=productlist.asp&Search_Hovedgruppe=&Search_Undergruppe=&Search_Producent=&Search_Type=&Search_Model=&Search_Plastic=&PriceFrom=&PriceTo=&Search_FREE={disc_search}', safe='?:/=&')
            driver.get(url)
            content = driver.page_source
            soup = BeautifulSoup(content, "html.parser")
            
            names = []
            manufacturers = []
            prices = []
            store = 'discconnection.dk'
            link = f'https://discconnection.dk/default.asp?page=productlist.asp&Search_Hovedgruppe=&Search_Undergruppe=&Search_Producent=&Search_Type=&Search_Model=&Search_Plastic=&PriceFrom=&PriceTo=&Search_FREE={disc_search}'

            # Contains: "Innova Firebird  •  Plastic: Champion  •  Driver"
            for prodHeader in soup.findAll("td", class_="prodHeader"):
                b = prodHeader.find_all("b")
                prodHeader_list = b[0].getText().split()
                manufacturers.append(prodHeader_list[0])
                names.append(b[0].getText())

            # Contains: Pris inkl. moms: 120,00 DKK
            for prodPriceWeight in soup.findAll("td", class_="prodPriceWeight"):
                b = prodPriceWeight.find("b")
                if b is not None:
                    prices.append(b.getText())            

            for i in range(len(names)):
                disc = self.Disc()
                disc.name = names[i]
                disc.manufacturer = manufacturers[i]
                disc.price = prices[i]
                disc.store = store
                disc.link = link
                self.discs.append(disc)  
