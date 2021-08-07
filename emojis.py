import re
from discord.ext import commands

def findWholeWord(w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

class Emojis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.disc_golf_words = ['disc', 'disc-golf', 'discgolf']

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id == 597085958244139022:
            for word in self.disc_golf_words:
                if findWholeWord(word)(message.content.lower()) is not None:
                    emoji = '<a:shutupandtakemymoney:751168620339527830>'
                    await message.add_reaction(emoji)
                    break 
        
            if 'bomb' in message.content.lower():
                emoji = '💣'
                await message.add_reaction(emoji)  
