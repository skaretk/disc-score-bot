import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from discord_utils.embed_validation import validate_embed
from scrapers.discgolfbagbuilder import DiscgolfBagBuilder
from .bagconfig import BagConfig

class Bag(commands.Cog):
    """Bag Class Cog"""
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="bag", description="Get bag from discgolfbagbuilder", guild_ids=[])
    async def bag_slash_command(self, interaction:Interaction):
        """/bag slash command"""

    @bag_slash_command.subcommand(name="show", description="Show your bag, or from another player")
    async def show(
        self,
        interaction:Interaction,
        user:nextcord.Member=SlashOption(description="user", required=False)
        ):
        """/bag show"""
        await interaction.response.defer()
        if user is None:
            user = interaction.user

        bag_scraper = self.scrape_bag(interaction.guild.name, user.id)
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

    @bag_slash_command.subcommand(name="add", description="Add or modify your bag from discgolfbagbuilder.com")
    async def add(
        self,
        interaction:Interaction,
        bag_url=SlashOption(description="discgolfbagbuilder.com url", required=True)
        ):
        """/bag add url"""
        user = interaction.user
        cfg = BagConfig(interaction.guild.name)
        modified = cfg.add_bag(user.id, bag_url)
        if modified:
            await interaction.response.send_message(f'Modified your bag {user.mention}')
        else:
            await interaction.response.send_message(f'Added your bag {user.mention}')

    def scrape_bag(self, guild_name, user):
        """Scrape user bag from discgolfbagbuilder.com"""
        cfg = BagConfig(guild_name)
        bag = cfg.get_bag(user)
        if bag is not None:
            bag_scraper = DiscgolfBagBuilder(bag)
            bag_scraper.scrape_discs()
            return bag_scraper
        return None

    def get_embed(self, bag_scraper):
        """Get bag embed"""
        embed = nextcord.Embed(title=bag_scraper.bag_name, description=bag_scraper.bag_description, url=bag_scraper.scrape_url, color=0x004899)
        embed.set_image(url="attachment://flight.png")

        if bag_scraper.distance_drivers:
            drivers = ''
            drivers_flights = ''
            for driver in bag_scraper.distance_drivers:
                drivers += f'[{driver}]({driver.url})\n'
                drivers_flights += f'{driver.flight}\n'
            embed.add_field(name="Drivers", value=drivers, inline=True)
            embed.add_field(name="Flight", value=drivers_flights, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
        if bag_scraper.fairway_drivers:
            fairways = ''
            fairways_flights = ''
            for fairway in bag_scraper.fairway_drivers:
                fairways += f'[{fairway}]({fairway.url})\n'
                fairways_flights += f'{fairway.flight}\n'
            embed.add_field(name="Fairways", value=fairways, inline=True)
            embed.add_field(name="Flight", value=fairways_flights, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
        if bag_scraper.midranges:
            midranges = ''
            midranges_flights = ''
            for midrange in bag_scraper.midranges:
                midranges += f'[{midrange}]({midrange.url})\n'
                midranges_flights += f'{midrange.flight}\n'
            embed.add_field(name="Midranges", value=midranges, inline=True)
            embed.add_field(name="Flight", value=midranges_flights, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
        if bag_scraper.putt_approach:
            putters = ''
            putters_flights = ''
            for putter in bag_scraper.putt_approach:
                putters += f'[{putter}]({putter.url})\n'
                putters_flights += f'{putter.flight}\n'
            embed.add_field(name="Putt and Approach", value=putters, inline=True)
            embed.add_field(name="Flight", value=putters_flights, inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            embed.set_footer(text="discgolfbagbuilder.com", icon_url=bag_scraper.icon_url)

        if validate_embed(embed):
            return embed
        return None
