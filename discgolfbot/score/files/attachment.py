import os
from nextcord.ext import commands
from score.files.scorecardreader import ScorecardReader

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
                
                    scorecard_reader = ScorecardReader(path, attachment.filename)
                    scorecard = scorecard_reader.parse()

                    embed = scorecard.get_embed(message.author.avatar.url)
                    if (embed != None):
                        await message.channel.send(embed=embed)
                    else:
                        message.channel.send("Scorecard stored, but scores is to big to display!")
                    
                    await message.delete()                    
