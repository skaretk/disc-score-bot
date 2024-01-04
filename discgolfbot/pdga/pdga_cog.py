
import nextcord
from nextcord.ext import commands
from nextcord.message import Attachment
from nextcord import Interaction, utils, embeds, emoji, slash_command, SlashOption, SlashCommandOption, Member

from discord_utils.embed_validation import *
from typing import Optional
from .pdgaPlayer import PdgaPlayer
from .pdgaPlayerNumberRelations import *
import re
from scrapers.pdga import PlayerProfileScraper, PdgaPlayerData

class PdgaPlayerStat(commands.Cog): 
    def __init__(self, discord_bot):
        self.bot = discord_bot
        self.config = {
            "pdga_player_uri": "https://www.pdga.com/player/",
            "db_file" : Path.joinpath(Path.cwd().parent, f'cfg/pdga_players.json') 
        }
        self.relations_handler = PdgaPlayerNumberRelations(db_file=self.config['db_file'])
        
    @nextcord.slash_command(name="pdga", description="all Pdga cog-commands", guild_ids=[]) 
    async def pdga_slash_command(self, interaction: Interaction):
        pass
    
    @pdga_slash_command.subcommand(name="set", description="add your pdga number to bot-db")
    async def set_pdga_number_slash_command(
        self,
        interaction: Interaction,
        pdga_number: int = SlashOption(name="setpdganumber", description="associate a pdga number with your discord-user", required=True, min_value=1, max_value=500000),
    ):

        if interaction.user.id in self.relations_handler.pdga_players:
            player_obj = self.relations_handler.player_objects[interaction.user.id]

            if pdga_number != player_obj.pdga_number:
                player_obj.pdga_number = pdga_number
                title = 'PDGA-number updated'
                msg = f"I've updated the pdga-number for your account, {interaction.user.mention}"
            else:
                title = 'PDGA-number unchanged'
                msg = f"Looks like you've already given me this exact number before, {interaction.user.mention}.\nTips: You can change your pdga number to any pdga-number you want, it doesn't really have to be yours"
        else:
            player_obj = PdgaPlayer(pdga_number=pdga_number,player_name=interaction.user.display_name, discord_id=interaction.user.id)
            msg = f"Thanks, {interaction.user.mention}! I've added pdga-number {pdga_number} to your account in my database"
            title = 'PDGA-number stored'
            self.relations_handler.add_relation(player_obj) 
        embed = nextcord.Embed(title=title, color=0x004899)
        embed.add_field(name="Set PDGA-number" ,value=msg, inline=False)
        if validate_embed(embed=embed):
            await interaction.send(embed=embed, content=f"{interaction.user.mention}:")
    
    @pdga_slash_command.subcommand(name="check", description="check the discord users pdga-bot info")
    async def check_pdga_number_slash_command(
        self,
        interaction: Interaction,
        discord_user: Optional[nextcord.Member] = SlashOption(name="user", description="name of discord-user to check", required=False),
    ):
        try:
            if discord_user == None:
                discord_user = interaction.user 
            if None == discord_user.nick:
                displayname = discord_user.name
            else:
                displayname = discord_user.nick
            if discord_user.id in self.relations_handler.pdga_players:
                embed_title = f"{displayname}'s pdga-bot info"
                embed = nextcord.Embed(title=embed_title, color=0x004899)
                dict_data = self.relations_handler.pdga_players[discord_user.id]
                embed_description_data = f"\nDiscord user: {dict_data['player_name']}\nPDGA Number: {dict_data['pdga_number']}"
                embed.description = embed_description_data 
            else:
                embed = nextcord.Embed(title=f"Uhm.. :thinking:", description=f"'{displayname}' hasn't told me their pdga-number yet", color=0x004899)
                await interaction.send(embed=embed,content=f"Sorry, I can't help you with this, {interaction.user.mention}")
        except:
            pass #FIXME: Do something
        finally:
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
        try:
            embed = self.get_www_pdga_com_user_data(pdga_player_number=pdga_number)  
        except:
            embed = nextcord.Embed(title="Oh, no! This didn't go very well :flushed:", color=0x004899)
        finally:
            if validate_embed(embed=embed):
                await interaction.send(embed=embed, content=f"{interaction.user.mention}:")

    @get_pdga_slash_command.subcommand(name="discorduser", description="get the discord users saved pdga number data from www.pdga.com info ")
    async def get_pdga_discord_user_slash_command(
        self,
        interaction: Interaction,
        discord_user: Optional[nextcord.Member] = SlashOption(name="discorduser", description="discord user's saved number to fetch from www.pdga.com",required=False)
    ):
        try:
            # user wants to retrieve own www.pdga.com info
            if discord_user == None:
                discord_user = interaction.user
            if discord_user.nick:
                displayname = discord_user.nick
            else:
                displayname = discord_user.name
            if discord_user.id in self.relations_handler.player_objects:
                pdga_player = self.relations_handler.player_objects[discord_user.id] #pdga_players[discord_user.id]
                embed = self.get_www_pdga_com_user_data(pdga_player_number=pdga_player.pdga_number)
            else:
                embed = nextcord.Embed(title=f"Hmmmmf.. :confused:", description=f"I must have misplaced the pdga-number for {displayname}", color=0x004899)
        except:
            embed = nextcord.Embed(title="Oh, no! This didn't go very well :flushed:", color=0x004899)
        finally:
            if validate_embed(embed=embed):
                await interaction.send(embed=embed, content=f"{interaction.user.mention}:")

    def get_www_pdga_com_user_data(
            self,
            pdga_player_number
    ):
        try:
            # construct the www.pdga.com/player/pdga_number scraper and start the scraping
            pdga_player_scraper = PlayerProfileScraper(pdga_number=f"{pdga_player_number}")
            pdga_player_scraper.scrape()

            if isinstance(pdga_player_scraper.player_data.player_name, str) and len(pdga_player_scraper.player_data.player_name) >= 3:
                embed_title = f"www.pdga.com - {pdga_player_scraper.player_data.player_name}"
            else:
                embed_title = f"Displaying '{pdga_player_scraper.scrape_url}'"
                
            embed = nextcord.Embed(title=embed_title, color=0x004899)
            if isinstance(pdga_player_scraper.player_data.portrait_url, str) and re.match(pattern="^https{0,1}://", string=pdga_player_scraper.player_data.portrait_url):
                embed.set_thumbnail(url=pdga_player_scraper.player_data.portrait_url)

            # call the PlayerDataObject's generate_dict method, creates custom headers 
            data_dict = pdga_player_scraper.player_data.generate_dict()

            # pass the data to the __process_embed_description_data method
            desc_contents = self.__process_embed_description_data__(pdga_player_data_dict=data_dict)
            embed.description = desc_contents

            # filter out the upcoming events, alternatively "N/A" in case there are none # TODO: need to write logic to limit / trim / split upcoming events data if there are too many
            upcoming_events_data = self.__process_upcoming_events_data__(pdga_player_data_dict=data_dict)
            embed.add_field(name="Upcoming events:", value=upcoming_events_data, inline=True)
        except:
            if not 'embed' in locals():
                embed_title = "Sorry, I couldn't find the embed I was attempting to work on :("
                embed = nextcord.Embed(title=embed_title, color=0x004899)
            else:
                embed_title = "Something went terribly wrong when I tried to get the pdga.com user data"
                embed = nextcord.Embed(title=embed_title, color=0x004899)
        finally:
            return embed
        
    def __process_upcoming_events_data__(self, pdga_player_data_dict:dict):
            if 'Upcoming Events' in pdga_player_data_dict and isinstance(pdga_player_data_dict, dict):
                if len(pdga_player_data_dict["Upcoming Events"]) >= 1:
                    return pdga_player_data_dict['Upcoming Events']
                else:
                    return "N/A"
                    # FIXME: Validate upcoming events content length 
                    pass
        
    def __process_embed_description_data__(self, pdga_player_data_dict:dict, key_long=17, value_long=55, total=62):
            desc_contents = ""
            for key in pdga_player_data_dict:
                if None == pdga_player_data_dict[key]:
                    continue
                if key == 'Upcoming Events':
                    continue
                insert = f"{pdga_player_data_dict[key].lstrip().rstrip()}"
                wordlength = len(f"{key}:{pdga_player_data_dict[key].lstrip().rstrip()}")
                add_value_spaces = value_long - wordlength
                add_key_spaces = key_long-len(key)
                insert_key_spaces = ""
                insert_value_spaces = ""
                if wordlength < total:
                    if len(key) > key_long:
                        insert_key_spaces = " "*add_key_spaces
                    if len(insert) < value_long:
                        insert_value_spaces = " "*add_value_spaces
                # embed_contents
                desc_contents += f"\n`{key}{insert_key_spaces}:{insert_value_spaces}{insert}`"
            return desc_contents