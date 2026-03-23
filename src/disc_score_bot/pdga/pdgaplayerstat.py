import re
import asyncio
import logging
from datetime import datetime, timedelta, time as dtime

logger = logging.getLogger(__name__)
from typing import Optional
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption, Embed, Member, TextChannel, slash_command
from disc_score_bot.utils.embed_validation import validate_embed
from disc_score_bot.scrapers.pdga import PlayerProfileScraper
from disc_score_bot.config import UserConfig, User, NotificationConfig, ClubPlayerConfig

class PdgaPlayerStat(commands.Cog):
    def __init__(self, discord_bot):
        self.bot = discord_bot
        self.check_upcoming_events.start()

    def cog_unload(self):
        self.check_upcoming_events.cancel()

    @slash_command(name="pdga", description="all Pdga cog-commands", guild_ids=[])
    async def pdga_slash_command(self, interaction: Interaction):
        pass

    @pdga_slash_command.subcommand(name="set", description="add your pdga number to bot-db")
    async def set_pdga_number_slash_command(
        self,
        interaction: Interaction,
        pdga_number: int = SlashOption(name="setpdganumber", description="associate a pdga number with your discord-user", required=True, min_value=1, max_value=500000),
    ):
        cfg = UserConfig(interaction.guild.name)
        user = cfg.get_user(interaction.user.id)
        if user is not None:
            user.pdga_number = pdga_number
        else:
            user = User(discord_id=interaction.user.id, pdga_number=pdga_number)

        written, modified = cfg.add_user(user)
        if written and modified:
            await interaction.response.send_message(f'Modified your pdga number{interaction.user.mention}')
        elif written:
            await interaction.response.send_message(f'Added your pdga number {interaction.user.mention}')
        else:
            await interaction.response.send_message(f'Failed to add your pdga number{interaction.user.mention}')

    @pdga_slash_command.subcommand(name="check", description="check the discord users pdga-bot info")
    async def check_pdga_number_slash_command(
        self,
        interaction: Interaction,
        discord_member: Optional[Member] = SlashOption(name="user", description="name of discord-user to check", required=False),
    ):
        if discord_member is None:
            discord_member = interaction.user

        cfg = UserConfig(interaction.guild.name)
        user = cfg.get_user(discord_id=discord_member.id)
        if user is not None:
            if user.pdga_number is not None:
                embed_title = f"{discord_member.display_name}'s pdga-bot info"
                embed = Embed(title=embed_title, description=f"\nPDGA Number: {user.pdga_number}", color=0x004899)
            else:
                embed = Embed(title="Uhm.. :thinking:", description=f"No pdga numer stored for '{discord_member.display_name}'", color=0x004899)
        else:
            embed = Embed(title="Uhm.. :thinking:", description=f"Could not find any configuration for '{discord_member.display_name}'", color=0x004899)

        if validate_embed(embed=embed):
            await interaction.send(embed=embed, content=f"{interaction.user.mention}:")

    @pdga_slash_command.subcommand(name="get", description="get the discord users www.pdga.com info")
    async def get_pdga_slash_command(self, interaction: Interaction):
        pass

    @get_pdga_slash_command.subcommand(name="pdganumber", description="get the discord users www.pdga.com info by pdga number")
    async def get_pdga_number_slash_command(
        self,
        interaction: Interaction,
        pdga_number: int = SlashOption(name="pdganumber", description="pdga-number to fetch from www.pdga.com",required=True, min_value=1, max_value=500000)
    ):
        embed = self.get_www_pdga_com_user_data(pdga_player_number=pdga_number)
        if embed is None:
            embed = Embed(title="Oh, no! This didn't go very well :flushed:", color=0x004899)

        if validate_embed(embed):
            await interaction.send(embed=embed, content=f"{interaction.user.mention}:")

    @get_pdga_slash_command.subcommand(name="discordmember", description="get the discord users saved pdga number data from www.pdga.com info ")
    async def get_pdga_discord_user_slash_command(
        self,
        interaction: Interaction,
        discord_member: Optional[Member] = SlashOption(name="discordmember", description="discord user's saved number to fetch from www.pdga.com", required=False)
    ):
        if discord_member is None:
            discord_member = interaction.user

        cfg = UserConfig(interaction.guild.name)
        user = cfg.get_user(discord_id=discord_member.id)
        if user is not None:
            if user.pdga_number is not None:
                embed = self.get_www_pdga_com_user_data(user.pdga_number)
            else:
                embed = Embed(title="Uhm.. :thinking:", description=f"No pdga numer stored for '{discord_member.display_name}'", color=0x004899)
        else:
            embed = Embed(title="Uhm.. :thinking:", description=f"Could not find any configuration for '{discord_member.display_name}'", color=0x004899)

        if validate_embed(embed):
            await interaction.send(embed=embed, content=f"{interaction.user.mention}:")

    @pdga_slash_command.subcommand(name="events", description="PDGA events notification settings")
    async def events_slash_command(self, interaction: Interaction):
        pass

    @events_slash_command.subcommand(name="set-channel", description="Set the channel for weekly upcoming PDGA event notifications")
    async def set_events_channel_slash_command(
        self,
        interaction: Interaction,
        channel: TextChannel = SlashOption(name="channel", description="Channel to post weekly notifications to", required=True),
    ):
        cfg = NotificationConfig(interaction.guild.name)
        if cfg.set_upcoming_events_channel_id(channel.id):
            await interaction.response.send_message(f"Upcoming PDGA event notifications will be sent to {channel.mention}")
        else:
            await interaction.response.send_message("Failed to save the notification channel.")

    @tasks.loop(time=dtime(hour=18, minute=0, tzinfo=datetime.now().astimezone().tzinfo))
    async def check_upcoming_events(self):
        """Weekly task (runs Thursdays at 18:00 local time): post Thu-Sun PDGA events for all registered users."""
        if datetime.now().weekday() != 3:  # 3 = Thursday
            return
        for guild in self.bot.guilds:
            channel_id = NotificationConfig(guild.name).get_upcoming_events_channel_id()
            if not channel_id:
                continue
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                continue

            users = ClubPlayerConfig(guild.name).read_module() or []
            embed = Embed(title="\U0001f4c5 Upcoming PDGA Events (Thu-Sun)", color=0x004899)
            found_any = False

            for user_data in users:
                pdga_number = user_data.get("pdga_number")
                if not pdga_number:
                    continue
                try:
                    scraper = PlayerProfileScraper(pdga_number=str(pdga_number))
                    scraper.scrape()
                    upcoming = [e for e in scraper.player_info.events.upcoming_events if self._is_upcoming_soon(e, days=3)]
                    if not upcoming:
                        continue
                    name = user_data.get("name") or str(pdga_number)
                    embed.add_field(name=name, value="\n".join(f"- {e}" for e in upcoming)[:1024], inline=False)
                    found_any = True
                except Exception as e:
                    logger.warning("Failed to check events for pdga#%s: %s", pdga_number, e)
                await asyncio.sleep(1)

            if found_any:
                await channel.send(embed=embed)

    @check_upcoming_events.before_loop
    async def before_check_upcoming_events(self):
        await self.bot.wait_until_ready()

    def _is_upcoming_soon(self, event, days: int = 3) -> bool:
        """Return True if the event starts within the next "days" (default covers Thu-Sun)."""
        date_start = getattr(event, 'date_start', None)
        if not date_start:
            return False
        try:
            date = datetime.strptime(date_start, "%a, %b %d, %Y")
            now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            return timedelta(0) <= (date - now) <= timedelta(days=days)
        except ValueError:
            return False

    def get_www_pdga_com_user_data(self, pdga_player_number):
        """construct the www.pdga.com/player/pdga_number scraper and start the scraping"""
        embed = None
        try:
            pdga_player_scraper = PlayerProfileScraper(pdga_number=f"{pdga_player_number}")
            pdga_player_scraper.scrape()

            if isinstance(pdga_player_scraper.player_info.player_name, str) and len(pdga_player_scraper.player_info.player_name) >= 3:
                embed_title = f'{pdga_player_scraper.player_info.player_name}'
            else:
                embed_title = f"Displaying '{pdga_player_scraper.scrape_url}'"

            embed = Embed(title=embed_title, url=pdga_player_scraper.scrape_url, color=0x004899)
            if isinstance(pdga_player_scraper.player_info.portrait_url, str) and re.match(pattern="^https{0,1}://", string=pdga_player_scraper.player_info.portrait_url):
                embed.set_thumbnail(url=pdga_player_scraper.player_info.portrait_url)
            else:
                embed.set_image(url='https://discord.com/assets/ee9c489e574f6ecb1d3c.svg')  # 🥏

            # pass the data to the __process_embed_description_data method
            desc_contents = self.__process_embed_description_data__(pdga_player_data_dict=pdga_player_scraper.player_info.dictionary)
            embed.description = desc_contents

            # filter out the upcoming events, alternatively "N/A" in case there are none
            upcoming_events_strings = self.__process_upcoming_events_data__(player_scraper_events=pdga_player_scraper.player_info.upcoming_events)

            for event_string in upcoming_events_strings:
                embed.add_field(name="Upcoming events:", value=event_string, inline=False)
        except:
            if embed is None:
                embed = Embed(title="Sorry, I couldn't find the embed I was attempting to work on :(", color=0x004899)
            else:
                embed = Embed(title="Something went terribly wrong when I tried to get the pdga.com user data", color=0x004899)
        finally:
            return embed

    def __process_upcoming_events_data__(self, player_scraper_events:list):
        upcoming_events_fields_values = []
        upcoming_events_string = ''
        for event in player_scraper_events:
            if len(upcoming_events_string) + len(f"{event}") > 1024:
                upcoming_events_fields_values.append(upcoming_events_string)
                upcoming_events_string = ''
            upcoming_events_string += f'\n- {event}'
        if len(upcoming_events_string) >=1:
            upcoming_events_fields_values.append(upcoming_events_string)
        return upcoming_events_fields_values

    def __process_embed_description_data__(self, pdga_player_data_dict:dict):
        key_long=17
        value_long=55
        total=62
        desc_contents = ""
        for key in pdga_player_data_dict:
            if pdga_player_data_dict[key] is None:
                continue
            if key == 'Upcoming Events':
                continue
            insert = f"{pdga_player_data_dict[key].strip()}"
            wordlength = len(f"{key}:{pdga_player_data_dict[key].strip()}")
            add_value_spaces = value_long - wordlength
            add_key_spaces = key_long-len(key)
            insert_key_spaces = ""
            insert_value_spaces = ""
            if wordlength < total:
                if len(key) > key_long:
                    insert_key_spaces = " "*add_key_spaces
                if len(insert) < value_long:
                    insert_value_spaces = " "*add_value_spaces
            desc_contents += f"\n`{key}{insert_key_spaces}:{insert_value_spaces}{insert}`"
        return desc_contents
