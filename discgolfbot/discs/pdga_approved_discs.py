import nextcord
from nextcord.ext import tasks, commands
from dateutil.parser import parse
import scrapers.pdga
from discord_utils.embed_validation import validate_embed
from .pdga_sql import PdgaSql

class PdgaApprovedDiscs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.search_discs.start()

    @tasks.loop(minutes=60.0)
    async def search_discs(self):
        new_approved_discs = []
        pdga_scraper = scrapers.pdga.DiscScraper()
        pdga_scraper.scrape()
        pdgaSql = PdgaSql()
        pdgaSql.create_table()
        storedDiscs = pdgaSql.get_discs()

        for disc in pdga_scraper.discs:
            if (disc not in storedDiscs):
                new_approved_discs.append(disc)
                pdgaSql.add_approved_disc(disc)
                print(f'NEW DISC: {disc.name} Stored in sql')
        
        # Any new approved discs?
        if new_approved_discs:
            embed = nextcord.Embed(title="New PDGA Approved Discs", color=0x004899)
            for disc in new_approved_discs:
                date = parse(disc.approved_date)
                embed.add_field(name=disc.manufacturer , value=f'[{disc.name}]({disc.url})\nDate: {date.strftime("%d.%m.%Y")}')#\n[Pdga Link]({disc.url})')       
                embed.set_thumbnail(url=(self.bot.user.avatar.url))

            # TODO: Configure channels to send event to
            #channel = self.bot.get_channel(905420670693949470) #Shim: bot
            channel = self.bot.get_channel(885087767292428298) #EDK: Disc Search
        
            await channel.send(embed=embed)

    # Wait for the bot to be ready before searching
    @search_discs.before_loop
    async def before_search(self):
        await self.bot.wait_until_ready()
