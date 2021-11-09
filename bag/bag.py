import discord
from discord.ext import commands
from bag.bags import Bags
from scrapers.discgolfbagbuilder import DiscgolfBagBuilder

class Bag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
    
    @commands.command(brief='bag [@user - optional]', description='%bag - Get your bag\n%bag @user - Get users bag')
    async def bag(self, ctx, user: discord.Member=None ):
        if (user == None):
            user = ctx.author
        bags = Bags(ctx.guild.name, user.display_name)
        bag = bags.get_player_bag()
        if (bag is not None):
            bag_scraper = DiscgolfBagBuilder(bag)
            bag_scraper.scrape_discs()
            await self.print_discs(ctx, bag_scraper)
        else:
            await ctx.send(f'Could not find any bag for player {user.display_name}')
    
    @commands.command(brief='bag_add [link]', description='Add your bag, or modify current bag-link')
    async def bag_add(self, ctx, bag_link):
        user = ctx.author
        bags = Bags(ctx.guild.name, user.display_name)
        modified = bags.add_player_bag(bag_link)
        if (modified == True):
            await ctx.send(f'Modified your bag {user.mention}')
        else:
            await ctx.send(f'Added your bag {user.mention}')
    
    async def print_discs(self, ctx, bag_scraper):
        embed = discord.Embed(title=bag_scraper.bag_name, description=bag_scraper.bag_description, url=bag_scraper.scrape_url, color=0xFF5733)
        file = discord.File(bag_scraper.image_file, filename="flight.png")
        embed.set_image(url="attachment://flight.png")

        if (len(bag_scraper.distance_drivers)):            
            drivers = ''
            driver_flights = ''
            for driver in bag_scraper.distance_drivers:
                drivers += f'[{driver}]({driver.url})\n'
                driver_flights += f'{driver.flight()}\n'
            embed.add_field(name="Drivers", value=drivers, inline=True)
            embed.add_field(name="Flight", value=driver_flights, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
        if (len(bag_scraper.fairway_drivers)):
            fairways = ''
            fairways_flights = ''
            for fairway in bag_scraper.fairway_drivers:
                fairways += f'[{fairway}]({fairway.url})\n'
                fairways_flights += f'{fairway.flight()}\n'
            embed.add_field(name="Fairways", value=fairways, inline=True)            
            embed.add_field(name="Flight", value=fairways_flights, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)          
        if (len(bag_scraper.midranges)):         
            midranges = ''
            midranges_flights = ''
            for midrange in bag_scraper.midranges:
                midranges += f'[{midrange}]({midrange.url})\n'
                midranges_flights += f'{midrange.flight()}\n'
            embed.add_field(name="Midranges", value=midranges, inline=True)
            embed.add_field(name="Flight", value=midranges_flights, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)  
        if (len(bag_scraper.fairway_drivers)):         
            putters = ''
            putters_flights = ''
            for putter in bag_scraper.putt_approach:
                putters += f'[{putter}]({putter.url})\n'
                putters_flights += f'{putter.flight()}\n'
            embed.add_field(name="Putt and Approach", value=putters, inline=True)
            embed.add_field(name="Flight", value=putters_flights, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)  
            embed.set_footer(text="Provided by discgolfbagbuilder.com", icon_url=bag_scraper.icon_url)

        if (len(embed) < 6000): # Size limit for embeds
            await ctx.send(file=file, embed=embed)
        else:
            print(len(embed))
            await ctx.send('https://giphy.com/embed/32mC2kXYWCsg0')
            await ctx.send('WOW, thats a lot of discs in the bag!')
