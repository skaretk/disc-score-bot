from discord.ext import commands
from csvreader import CsvReader
import os

class Attachment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        path = str(f'{message.guild.name}\{message.channel}')
    
        # any attachments in the message?
        if message.attachments:
            for attachment in message.attachments:
                if 'text/csv' in attachment.content_type:
                    if not os.path.exists(path):
                        os.makedirs(path)
                    await attachment.save(fp=f"{path}\{attachment.filename}") # saves the file in a server/channel folder
                    print(f'csv attached and stored in {path}\{attachment.filename}!')
                
                    csvreader = CsvReader(path, attachment.filename)
                    scorecard = csvreader.parse()
                
                    await message.channel.send(embed=scorecard.get_embed_full(message.author.avatar_url))
                    await message.delete()
                    return
