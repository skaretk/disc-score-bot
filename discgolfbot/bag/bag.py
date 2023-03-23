import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from discord_utils.embed_validation import validate_embed
from scrapers.discgolfbagbuilder import DiscgolfBagBuilder
from .bags import Bags

class Bag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands
    @commands.command(name="bag", brief='bag [@user - optional]', description='%bag - Get your bag\n%bag @user - Get users bag')
    async def bag_command(self, ctx, user: nextcord.Member=None ):
        if (user == None):
            user = ctx.author

        bag_scraper = self.scrape_bag(ctx.guild.name, user.display_name)
        if bag_scraper is not None:
            embed = self.get_embed(bag_scraper)
            if embed is not None:
                file = nextcord.File(bag_scraper.image_file, filename="flight.png")
                await ctx.send(file=file, embed=embed)
            else:
                await ctx.send('https://giphy.com/embed/32mC2kXYWCsg0')
                await ctx.send('WOW, thats a lot of discs in the bag!')
        else:
            await ctx.send(f'Could not find any bag for player {user.display_name}')

    @commands.command(name="bag_add", brief='bag_add [link]', description='Add your bag, or modify current bag-link')
    async def bag_add_command(self, ctx, bag_link):
        user = ctx.author
        bags = Bags(ctx.guild.name, user.display_name)
        modified = bags.add_player_bag(bag_link)
        if (modified == True):
            await ctx.send(f'Modified your bag {user.mention}')
        else:
            await ctx.send(f'Added your bag {user.mention}')

    # Slash command bag
    @nextcord.slash_command(name="bag", description="Get bag from discgolfbagbuilder", guild_ids=[])
    async def bag_slash_command(self, interaction: Interaction):
        pass

    @bag_slash_command.subcommand(name="show", description="Show your bag, or from another player")
    async def bag_show_slash_command(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="user", required=False)):
        await interaction.response.defer()
        if (user == None):
            user = interaction.user

        bag_scraper = self.scrape_bag(interaction.guild.name, user.display_name)
        if bag_scraper is not None:
            embed = self.get_embed(bag_scraper)
            if embed is not None:
                file = nextcord.File(bag_scraper.image_file, filename="flight.png")
                await interaction.followup.send(file=file, embed=embed)
            else:
                await interaction.followup.send('https://giphy.com/embed/32mC2kXYWCsg0')
                await interaction.followup.send('WOW, thats a lot of discs in the bag!')
        else:
            await interaction.followup.send(f'Could not find any bag for player {user.display_name}')

    @bag_slash_command.subcommand(name="add_link", description="Add your bag, or modify current bag-link")
    async def bag_link_slash_command(self, interaction: Interaction, bag_link = SlashOption(description="discgolfbagbuilder.com link", required=True)):
        user = interaction.user
        bags = Bags(interaction.guild.name, user.display_name)
        modified = bags.add_player_bag(bag_link)
        if (modified == True):
            await interaction.response.send_message(f'Modified your bag {user.mention}')
        else:
            await interaction.response.send_message(f'Added your bag {user.mention}')

    def scrape_bag(self, guild_name, user):
        bags = Bags(guild_name, user)
        bag = bags.get_player_bag()
        if (bag is not None):
            bag_scraper = DiscgolfBagBuilder(bag)
            bag_scraper.scrape_discs()
            return bag_scraper
        return None

    def get_embed(self, bag_scraper):
        embed = nextcord.Embed(title=bag_scraper.bag_name, description=bag_scraper.bag_description, url=bag_scraper.scrape_url, color=0x004899)
        embed.set_image(url="attachment://flight.png")

        if (len(bag_scraper.distance_drivers)):
            drivers = ''
            drivers_flights = ''
            for driver in bag_scraper.distance_drivers:
                drivers += f'[{driver}]({driver.url})\n'
                drivers_flights += f'{driver.flight}\n'
            embed.add_field(name="Drivers", value=drivers, inline=True)
            embed.add_field(name="Flight", value=drivers_flights, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
        if (len(bag_scraper.fairway_drivers)):
            fairways = ''
            fairways_flights = ''
            for fairway in bag_scraper.fairway_drivers:
                fairways += f'[{fairway}]({fairway.url})\n'
                fairways_flights += f'{fairway.flight}\n'
            embed.add_field(name="Fairways", value=fairways, inline=True)
            embed.add_field(name="Flight", value=fairways_flights, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
        if (len(bag_scraper.midranges)):
            midranges = ''
            midranges_flights = ''
            for midrange in bag_scraper.midranges:
                midranges += f'[{midrange}]({midrange.url})\n'
                midranges_flights += f'{midrange.flight}\n'
            embed.add_field(name="Midranges", value=midranges, inline=True)
            embed.add_field(name="Flight", value=midranges_flights, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
        if (len(bag_scraper.fairway_drivers)):
            putters = ''
            putters_flights = ''
            for putter in bag_scraper.putt_approach:
                putters += f'[{putter}]({putter.url})\n'
                putters_flights += f'{putter.flight}\n'
            embed.add_field(name="Putt and Approach", value=putters, inline=True)
            embed.add_field(name="Flight", value=putters_flights, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.set_footer(text="Provided by discgolfbagbuilder.com", icon_url=bag_scraper.icon_url)

        # Validate and return embed
        if validate_embed(embed):
            return embed
        return None
