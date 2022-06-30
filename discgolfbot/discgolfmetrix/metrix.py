from datetime import datetime
import time
from nextcord import Interaction, SlashOption
import nextcord
from nextcord.ext import commands
from apis.discgolfmetrixapi import DiscgolfMetrixApi
from .metrixplayer import MetrixPlayer
from .metrixcompetition import MetrixCompetition
from .metrixcompetitions import MetrixCompetitions
from .metrixcourse import MetrixCourse

class Metrix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['Metrix'], pass_context=True, brief='Discgolf Metrix API functions', description='See subcommands')
    async def metrix(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @metrix.command(brief='Add your player code', description='Add your metrix player code from metrix account')
    async def add_player_code(self, ctx, player_code):
        user = ctx.author
        metrix_player = MetrixPlayer(ctx.guild.name, user.display_name)
        modified = metrix_player.add_player_code(player_code)
        if (modified == True):
            await ctx.send(f'Modified your metrix player code {user.mention}')
        else:
            await ctx.send(f'Added your metrix player code {user.mention}')

    @metrix.command(brief='Search course by ID', description='Search for course on discgolfmetrix by ID')
    async def search_course_id(self, ctx, course_id):
        api = DiscgolfMetrixApi()
        json = api.course(course_id, "HtDz6uLTsF76bFmCGToVsNe9khDf3sJA")
        if json is not None:
            course = MetrixCourse(json)
            embed = course.get_embed()

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Could not find the course')

    @metrix.command(brief='List my competitions, or a players competitions', description='Lists out competitions for you, or a given player')
    async def competitions(self, ctx, user: nextcord.Member=None ):
        start_time = time.time()
        if (user == None):
            user = ctx.author
        player = MetrixPlayer(ctx.guild.name, user.display_name)
        code = player.get_player_code()

        if (code is not None):
            api = DiscgolfMetrixApi()
            json = api.my_competitions(code)
            competitions = MetrixCompetitions()
            for competition in json.get("my_competitions"):
                comptetition_json = api.get_results(competition)
                if comptetition_json is not None:
                    metrix_competition = MetrixCompetition(comptetition_json)
                    if metrix_competition.is_valid():
                        if datetime.today().date() <= metrix_competition.datetime.date():
                            competitions.add_competition(metrix_competition)

            embed = competitions.get_embed()

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Could not find your player code {user.display_name}, please add it by using %metrix add_player code')

        cmd_time = time.time() - start_time
        print(f'my_competitions: {cmd_time}')

    # Slash commands
    @nextcord.slash_command(name="metrix", description="Discgolfmetrix commands", guild_ids=[])
    async def metrix_slash_command(self):
        pass

    @metrix_slash_command.subcommand(name="add_player_code", description="Add your discgolfmetrix player code")
    async def add_player_code_slash_command(
        self,
        interaction: Interaction,
        player_code: str = SlashOption(name="code", description="Player code from discgolfmetrix", required=True)
    ):
        user = interaction.user
        metrix_player = MetrixPlayer(interaction.guild, user.display_name)
        modified = metrix_player.add_player_code(player_code)
        if (modified == True):
            await interaction.response.send_message(f'Modified your metrix player code {user.mention}')
        else:
            await interaction.response.send_message(f'Added your metrix player code {user.mention}')