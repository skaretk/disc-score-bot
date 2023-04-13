from concurrent.futures import ThreadPoolExecutor
from typing import Optional
import time
from datetime import datetime
from apis.discgolfmetrixapi import DiscgolfMetrixApi
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from .discgolfmetrixconfig import DiscgolfmetrixConfig
from .discgolfmetrixcompetition import DiscgolfmetrixCompetition
from .discgolfmetrixcompetitions import DiscgolfmetrixCompetitions
from .discgolfmetrixcourse import DiscgolfmetrixCourse, DiscgolfmetrixCourseSource
from .discgolfmetrixcourses import DiscgolfmetrixCourses

class DiscgolfMetrix(commands.Cog):
    '''Discgolfmetrix Cog'''
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="discgolfmetrix", description="Discgolfmetrix commands", guild_ids=[])
    async def discgolfmetrix_slash_command(self):
        '''/discgolfmetrix'''

    @discgolfmetrix_slash_command.subcommand(name="add_player_code", description="Add your discgolfmetrix player code")
    async def add_player_code(
        self,
        interaction:Interaction,
        player_code:str = SlashOption(name="code", description="Player code from discgolfmetrix", required=True)
    ):
        '''/discgolfmetrix add_player_code'''
        user = interaction.user
        cfg = DiscgolfmetrixConfig(interaction.guild)
        modified = cfg.add_code(user.id, player_code)
        if modified:
            await interaction.response.send_message(f'Modified your discgolfmetrix player code {user.mention}')
        else:
            await interaction.response.send_message(f'Added your discgolfmetrix player code {user.mention}')

    @discgolfmetrix_slash_command.subcommand(name="competitions", description="Lists your competitions, or for a given player")
    async def competitions(
        self,
        interaction:Interaction,
        user: Optional[nextcord.Member] = SlashOption(name="player", description="Player name", required=False)
    ):
        '''/discgolfmetrix competitions'''
        await interaction.response.defer()

        start_time = time.time()
        if user is None:
            user = interaction.user
        cfg = DiscgolfmetrixConfig(interaction.guild)
        code = cfg.get_code(user.id)

        if code is not None:
            api = DiscgolfMetrixApi()
            json = api.my_competitions(code)
            competitions = DiscgolfmetrixCompetitions()
            competition_list = []
            for competition in json.get("my_competitions"):
                competition_list.append(competition)
            print(f'Found {len(competition_list)} competitions')

            future_list = []
            with ThreadPoolExecutor(max_workers=len(competition_list)) as executor:
                for competition_item in enumerate(competition_list):
                    future_list.append(executor.submit(api.get_results, competition_item))

            for future in future_list:
                if future.result() is not None:
                    competition = DiscgolfmetrixCompetition(future.result())
                    if competition.is_valid():
                        if datetime.today().date() <= competition.datetime.date():
                            competitions.add_competition(competition)

            embed = competitions.get_embed()

            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f'Could not find your player code {user.mention}, please add it by using [/metrix add_player_code]')

        print(f'competitions: {round(time.time() - start_time, 2)}')

    @discgolfmetrix_slash_command.subcommand(name='search_course_id', description='Search for course on discgolfmetrix by ID')
    async def search_course_id(
        self,
        interaction:Interaction,
        course_id: str = SlashOption(name="course", description="Course ID from discgolfmetrix", required=True)
    ):
        '''/discgolfmetrix search_course_id'''
        api = DiscgolfMetrixApi()
        user = interaction.user
        cfg = DiscgolfmetrixConfig(interaction.guild)
        code = cfg.get_code(user.id)
        if code is not None:
            json = api.course(course_id, code)
            if json is not None:
                course = DiscgolfmetrixCourse(json, DiscgolfmetrixCourseSource.ID)
                embed = course.get_embed()
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message('Could not find the course')
        else:
            await interaction.response.send_message(f'Could not find your player code {user.mention}, please add it by using [/metrix add_player_code]')

    @discgolfmetrix_slash_command.subcommand(name='search_course_name', description='Search for course on discgolfmetrix by name')
    async def search_course_name(
        self,
        interaction:Interaction,
        course_name:str = SlashOption(name="course", description="Course name", required=True)
    ):
        '''/discgolfmetrix search_course_name'''
        api = DiscgolfMetrixApi()
        json = api.courses_list("NO", course_name)
        if json is not None:
            courses = json.get("courses")
            metrix_courses = DiscgolfmetrixCourses()
            for course in courses:
                metrix_courses.add_course(DiscgolfmetrixCourse(course, DiscgolfmetrixCourseSource.LIST))

            embed = metrix_courses.get_embed()

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message('Could not find the course')
