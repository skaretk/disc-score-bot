from nextcord.ext import commands
import re

def findWholeWord(w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

class Emojis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.disc_golf_words = ['disc', 'disc-golf', 'discgolf']
        self.ace_golf_words = ['ace', 'aces', 'aca', 'aced']
        self.beer_words = ['øl', 'beer', 'berras']

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id == 885085437448839209: # EDK
            for word in self.disc_golf_words:
                if findWholeWord(word)(message.content.lower()) is not None:
                    emoji = '<a:shutupandtakemymoney:897176782346784778>'
                    await message.add_reaction(emoji)
                    break
        
            if 'bomb' in message.content.lower():
                emoji = '💣'
                await message.add_reaction(emoji)  

            if 'discs' in message.content.lower():
                emoji = '🥏'
                await message.add_reaction(emoji)
            
            for word in self.ace_golf_words:
                if findWholeWord(word)(message.content.lower()) is not None:
                    emoji = '<a:ace:897177537908703232>'
                    await message.add_reaction(emoji)  
                    break
            
            for word in self.beer_words:
                if findWholeWord(word)(message.content.lower()) is not None:
                    emoji = '🍻'
                    await message.add_reaction(emoji)  
                    break
