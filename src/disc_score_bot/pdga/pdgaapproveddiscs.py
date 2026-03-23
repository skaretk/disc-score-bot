import nextcord
from nextcord.ext import tasks, commands
from dateutil.parser import parse
import logging
from disc_score_bot.scrapers import pdga
from disc_score_bot.config import NotificationConfig
from .pdgaapproveddiscssql import PdgaSql

logger = logging.getLogger(__name__)

class PdgaApprovedDiscs(commands.Cog):
    """PdgaApprovedDiscs Cog"""
    def __init__(self, bot):
        self.bot = bot
        self.search_discs.start()

    @tasks.loop(minutes=60.0)
    async def search_discs(self):
        """Search for pdga approved discs"""
        new_approved_discs = []
        pdga_scraper = pdga.DiscScraper()
        pdga_scraper.scrape()
        pdga_sql = PdgaSql()
        pdga_sql.create_table()
        stored_discs = pdga_sql.get_discs()

        for disc in pdga_scraper.discs:
            if disc not in stored_discs:
                new_approved_discs.append(disc)
                pdga_sql.add_approved_disc(disc)
                logger.info('NEW DISC: %s Stored in sql', disc.name)

        # Any new approved discs?
        if new_approved_discs:
            embed = nextcord.Embed(title="New PDGA Approved Discs", color=0x004899)
            for disc in new_approved_discs:
                date = parse(disc.approved_date)
                embed.add_field(name=disc.manufacturer, value=f'[{disc.name}]({disc.url})\nDate: {date.strftime("%d.%m.%Y")}')#\n[Pdga Link]({disc.url})')
                embed.set_thumbnail(url=(self.bot.user.avatar.url))

            # Send to configured channel per guild
            for guild in self.bot.guilds:
                channel_id = NotificationConfig(guild.name).get_new_pdga_approved_discs_channel_id()
                channel = self.bot.get_channel(channel_id) if channel_id else None
                if channel:
                    await channel.send(embed=embed)

    # Wait for the bot to be ready before searching
    @search_discs.before_loop
    async def before_search(self):
        """Preconditions for searching"""
        await self.bot.wait_until_ready()
