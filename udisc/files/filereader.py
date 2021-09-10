from discord.ext import commands
import utilities
import os

class FileReader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='List stored files', description='Lists all files stored in this discord server and channel')
    async def files(self, ctx):
        path = str(f'{ctx.guild.name}\{ctx.channel}')

        if utilities.is_path_empty(path):
            await ctx.send('No files stored for this channel')
            return
        
        msg_to_send = ''
        file_count = 0
        for file in os.listdir(path):
            if file.endswith(".csv"):
                file_count += 1
                print(os.path.join(f'{path}\{file}'))
                msg_to_send += f'\n{file}'
    
        if file_count:     
            await ctx.send(f'No of files: {file_count}\n{msg_to_send}')
        else:
            await ctx.send('No .csv files stored for this channel')
