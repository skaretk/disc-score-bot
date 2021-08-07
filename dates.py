from discord.ext import commands
from csvreader import CsvReader
import utilities
import os

class Dates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dates(self, ctx):
        path = str(f'{ctx.guild.name}\{ctx.channel}')

        if utilities.is_path_empty(path):
            await ctx.send("No scores stored for this channel")
            return
    
        # Get current dates
        datelist = []
        for file in os.listdir(path):
            if file.endswith(".csv"):
                csvreader = CsvReader(path, file)
                scorecard = csvreader.parse()

                date = scorecard.date_time.date()

                if date not in datelist:
                    datelist.append(date)
    
        msg = ''
        for date in datelist:
            msg += f'\n{date}'

        await ctx.send(msg)
