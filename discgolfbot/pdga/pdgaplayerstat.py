import re
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Embed, Member, slash_command
from discord_utils.embed_validation import validate_embed
from scrapers.pdga import PlayerProfileScraper
from .pdgaplayer import PdgaPlayer
from .pdgaplayerconfig import PdgaPlayerConfig

class PdgaPlayerStat(commands.Cog):
    def __init__(self, discord_bot):
        self.bot = discord_bot

    @slash_command(name="pdga", description="all Pdga cog-commands", guild_ids=[])
    async def pdga_slash_command(self, interaction: Interaction):
        pass

    @pdga_slash_command.subcommand(name="set", description="add your pdga number to bot-db")
    async def set_pdga_number_slash_command(
        self,
        interaction: Interaction,
        pdga_number: int = SlashOption(name="setpdganumber", description="associate a pdga number with your discord-user", required=True, min_value=1, max_value=500000),
    ):
        cfg = PdgaPlayerConfig(interaction.guild.name)
        written, modified = cfg.add_user(PdgaPlayer(interaction.user.id, pdga_number))
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
        discord_user: Optional[Member] = SlashOption(name="user", description="name of discord-user to check", required=False),
    ):
        if discord_user is None:
            discord_user = interaction.user

        cfg = PdgaPlayerConfig(interaction.guild.name)
        pdga_number = cfg.get_pdga_number(discord_user.id)
        if pdga_number is not None:
            embed_title = f"{discord_user.display_name}'s pdga-bot info"
            embed = Embed(title=embed_title, color=0x004899)
            embed.description = f"\nPDGA Number: {pdga_number}"
        else:
            embed = Embed(title="Uhm.. :thinking:", description=f"'{discord_user.display_name}' hasn't told me their pdga-number yet", color=0x004899)
            await interaction.send(embed=embed,content=f"Sorry, I can't help you with this, {interaction.user.mention}")

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

    @get_pdga_slash_command.subcommand(name="discorduser", description="get the discord users saved pdga number data from www.pdga.com info ")
    async def get_pdga_discord_user_slash_command(
        self,
        interaction: Interaction,
        discord_user: Optional[Member] = SlashOption(name="discorduser", description="discord user's saved number to fetch from www.pdga.com", required=False)
    ):
        embed = None
        if discord_user is None:
            discord_user = interaction.user

        cfg = PdgaPlayerConfig(interaction.guild.name)
        pdga_number = cfg.get_pdga_number(discord_user.id)

        if pdga_number is not None:
            embed = self.get_www_pdga_com_user_data(pdga_number)
        else:
            embed = Embed(title="Hmmmmf.. :confused:", description=f"I must have misplaced the pdga-number for {discord_user.displayname}", color=0x004899)

        if embed is None:
            embed = Embed(title="Oh, no! This didn't go very well :flushed:", color=0x004899)
        if validate_embed(embed):
            await interaction.send(embed=embed, content=f"{interaction.user.mention}:")

    def get_www_pdga_com_user_data(self, pdga_player_number):
        """construct the www.pdga.com/player/pdga_number scraper and start the scraping"""
        embed = None
        try:
            pdga_player_scraper = PlayerProfileScraper(pdga_number=f"{pdga_player_number}")
            pdga_player_scraper.scrape()

            if isinstance(pdga_player_scraper.player_data.player_name, str) and len(pdga_player_scraper.player_data.player_name) >= 3:
                embed_title = f'{pdga_player_scraper.player_data.player_name}'
            else:
                embed_title = f"Displaying '{pdga_player_scraper.scrape_url}'"

            embed = Embed(title=embed_title, url=pdga_player_scraper.scrape_url, color=0x004899)
            if isinstance(pdga_player_scraper.player_data.portrait_url, str) and re.match(pattern="^https{0,1}://", string=pdga_player_scraper.player_data.portrait_url):
                embed.set_thumbnail(url=pdga_player_scraper.player_data.portrait_url)
            else:
                embed.set_image(url='https://discord.com/assets/ee9c489e574f6ecb1d3c.svg')  # 🥏

            # pass the data to the __process_embed_description_data method
            desc_contents = self.__process_embed_description_data__(pdga_player_data_dict=pdga_player_scraper.player_data.dictionary)
            embed.description = desc_contents

            # filter out the upcoming events, alternatively "N/A" in case there are none
            upcoming_events_strings = self.__process_upcoming_events_data__(player_scraper_events=pdga_player_scraper.player_data.upcoming_events)

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