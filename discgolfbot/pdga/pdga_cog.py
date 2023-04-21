
import nextcord
from nextcord.ext import commands
from nextcord.message import Attachment
from nextcord import Interaction, utils, embeds, emoji, slash_command, SlashOption, SlashCommandOption
from discord_utils.embed_validation import *
from typing import Optional
from .pdgaPlayer import PdgaPlayer
from .pdgaPlayerNumberRelations import *
import re
from scrapers.pdga import PlayerScraper, PdgaPlayerData

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
        pdga_number: int = SlashOption(name="setpdganumber", description="associate a pdga number with your discord-user", required=True),
    ):

        player_obj = PdgaPlayer(pdga_number=pdga_number,player_name=interaction.user.display_name, discord_id=interaction.user.id)
        if player_obj.pdga_number in self.relations_handler.pdga_numbers:
            
            if self.relations_handler.pdga_numbers[pdga_number].discord_id != interaction.user.id:
                diff_player = self.relations_handler.pdga_numbers[pdga_number]
                title = 'Whoopsie!'
                msg = f"Hey, {interaction.user.mention}. Looks like this pdga-number belongs to @{diff_player.player_name} , are you sure this was the correct pdga-number?"
            else:
                title = 'All good!'
                msg = f"Hey, {interaction.user.mention}. I already have your pdga-number"
        else:
            msg = f"Sweet, {interaction.user.mention}! I've added your pdga-number"
            title = 'Done and done'
            self.relations_handler.add_relation(player_obj) 
        embed = nextcord.Embed(title=title, color=0x004899)
        embed.add_field(name="Pdga number added" ,value=msg, inline=False)
        if validate_embed(embed=embed):
            await interaction.send(embed=embed, content=f"{interaction.user.mention}:")
    
    @pdga_slash_command.subcommand(name="check", description="check the discord users pdga-bot info")
    async def check_pdga_number_slash_command(
        self,
        interaction: Interaction,
        displayname: Optional[str] = SlashOption(name="displayname", description="name of discord-user to check", required=False),
    ):
        try:
            user_id = interaction.user.id
            
            if not isinstance(displayname, str):
                user_id = interaction.user.id
                displayname = interaction.user.nick
            
            user = self.__get_user_by_nick__(interaction=interaction,nick=displayname)
            if user:
                user_id = user.id
                if None == user.nick:
                    displayname = user.name
                else:
                    displayname = user.nick
            if user_id in self.relations_handler.by_discord_id:
            
                embed_title = f"{displayname}'s pdga-bot info"
                embed = nextcord.Embed(title=embed_title, color=0x004899)
                obj = self.relations_handler.pdga_players[displayname].to_dict()
                out = f"\nDiscord user: {obj['player_name']}\nPDGA Number: {obj['pdga_number']}"
                embed.description = out # .add_field(name=segment, value=out, inline=False)

            else:
                embed = nextcord.Embed(title=f"Uhm.. :confused:", description=f"I don't know of a discord-user whoose name is '{displayname}'", color=0x004899)
                await interaction.send(embed=embed,content=f"Sorry, {interaction.user.mention}!")
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
            embed = await self.get_www_pdga_com_user_data(pdga_player_number=pdga_number)  
        except:
            embed = nextcord.Embed(title="Oh, no! This didn't go very well :flushed:", color=0x004899)
        finally:
            if validate_embed(embed=embed):
                await interaction.send(embed=embed, content=f"{interaction.user.mention}:")

    @get_pdga_slash_command.subcommand(name="discorduser", description="get the discord users saved pdga number data from www.pdga.com info ")
    async def get_pdga_discord_user_slash_command(
        self,
        interaction: Interaction,
        discord_user: Optional[str] = SlashOption(name="discorduser", description="discord user's saved number to fetch from www.pdga.com",required=False)
    ):
        try:
            # user wants to retrieve own www.pdga.com info
            if discord_user == None:
                user = interaction.user
            else:
                user = self.__get_user_by_nick__(interaction=interaction, nick=discord_user)
            if user and (user.id in self.relations_handler.by_discord_id):
                pdga_player = self.relations_handler.by_discord_id[user.id]
                embed = self.get_www_pdga_com_user_data(pdga_player_number=pdga_player.pdga_number)
            else:
                embed = nextcord.Embed(title=f"Hmmmmf.. :confused:", description=f"I must have misplaced the pdga-number for {user.nick}", color=0x004899)
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
            pdga_player_scraper = PlayerScraper(pdga_number=f"{pdga_player_number}")

            pdga_player_data = pdga_player_scraper.scrape()

            if isinstance(pdga_player_data.player_name, str) and len(pdga_player_data.player_name) >= 3:
                embed_title = "www.pdga.com - {}".format(pdga_player_data.player_name)
            else:
                embed_title = "www.pdga.com player information"
                
            embed = nextcord.Embed(title=embed_title, color=0x004899)
            if isinstance(pdga_player_data.portrait_url, str) and re.match(pattern="^https{0,1}://", string=pdga_player_data.portrait_url):
                embed.set_thumbnail(url=pdga_player_data.portrait_url)

            embed_contents = "" 
            desc_contents = ""
            key_long = 17
            value_long = 55
            total = 62
            pdga_player_data_dict = pdga_player_data.prettify()
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
            embed.description = desc_contents #f"```elm\n{desc_contents}```"  # Player bio:\n\n


            if 'Upcoming Events' in pdga_player_data_dict:
                if len(pdga_player_data_dict["Upcoming Events"]) >= 1:
                    embed.add_field(name="Upcoming events:", value=pdga_player_data_dict['Upcoming Events'], inline=True)
                    #embed.description = f"Upcoming events: \n\n{pdga_player_data_dict[key]}"
                    # FIXME: Validate upcoming events content length 
                    pass
        except:
            if not 'embed' in locals():
                embed_title = "Sorry, I failed you :("
                embed = nextcord.Embed(title=embed_title, color=0x004899)
        finally:
            return embed
        
    def __get_user_by_nick__(self, interaction: Interaction, nick):
        try:
            user= nextcord.utils.get(interaction.guild.members, nick=nick)
            if None == user:
                user= nextcord.utils.get(interaction.guild.members, name=nick)
        except:
            user = False
        finally:
            return user