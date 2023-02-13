import os
from nextcord.ext import commands
from score.files.udisccsvreader import UdiscCsvReader

class Attachment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        path = str(f'{os.getcwd()}/cfg/{message.guild.name}/{message.channel}')

        # any attachments in the message?
        if message.attachments:
            for attachment in message.attachments:
                if 'text/csv' in attachment.content_type:
                    if not os.path.exists(path):
                        os.makedirs(path)
                    await attachment.save(fp=f"{path}/{attachment.filename}") # saves the file in a server/channel folder
                    print(f'csv attached and stored in {path}/{attachment.filename}!')

                    reader = UdiscCsvReader(path, attachment.filename)
                    scorecard = reader.parse()

                    if scorecard is None:
                        await message.channel.send("Scorecard stored, but could not parse scorecard!")
                    else:
                        embed = scorecard.get_embed(message.author.avatar.url)
                        if embed is not None:
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send("Scorecard stored, but scores is to big to display!")

                    await message.delete()
