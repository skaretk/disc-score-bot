import discord
from discord.ext import commands

import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from scraper import Scraper

class Flight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Get disc flightpath', description='Prints the flightpath of a disc')
    async def flight(self, ctx, *args, sep=" "):
        if len(args) == 0:
            await ctx.send('No disc specified, see %help flight')
            return

        disc_search = sep.join(args)
        disc_name = ''
        img_url = ''
        disc_speed = ''
        disc_glide = ''
        disc_turn = ''
        disc_fade = ''

        start_time = time.time()
        with Scraper.get_chrome(self) as driver:
            url = urllib.parse.quote("https://www.marshallstreetdiscgolf.com/flightguide", safe='?:/=')
            driver.get(url)
            time.sleep(1)
            content = driver.page_source
            soup = BeautifulSoup(content, "html.parser")

            for disc in soup.findAll("div", class_="flex-grid-item disc-item"):
                if (disc.getText().lower() == disc_search.lower()):
                    disc_name = disc.getText()
                    img_url = disc['data-pic']
                    disc_speed = disc['data-speed']
                    disc_glide = disc['data-glide']
                    disc_turn = disc['data-turn']
                    disc_fade = disc['data-fade']
                    break
            for putter in soup.findAll("div", class_="putter-child pc-entry"):
                putter_name = putter['data-putter']
                if (putter_name.lower() == disc_search.lower()):
                    disc_name = putter_name
                    img_url = putter['data-image']
                    disc_speed = putter['data-speed']
                    disc_glide = putter['data-glide']
                    disc_turn = putter['data-turn']
                    disc_fade = putter['data-fade']
                    break
        end_time = time.time()
        print(f'Spent {end_time - start_time} scraping')

        if img_url != '':
            embed = discord.Embed(title=disc_name, color=0xFF5733)
            embed.add_field(name='Flight', value=f'Speed: {disc_speed} Glide:{disc_glide} Turn: {disc_turn} Fade: {disc_fade}', inline=True)    
            embed.set_image(url=img_url)
            embed.set_thumbnail(url=(ctx.author.avatar_url))
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Could not find flight path for {disc_search} {ctx.author.mention}')  
