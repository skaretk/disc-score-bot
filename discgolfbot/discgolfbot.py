import discord
from discord.ext import commands
from discord.message import Attachment

# Fetch python bot token
from dotenv import load_dotenv, find_dotenv
from os import getenv

# cogs
from score.files.attachment import Attachment
from score import Scores
from emoji import Emojis
from discs import Discs
from bag import Bag

# discord client
def main():
    print("main()")
    load_dotenv(find_dotenv('token.env'))
    token = getenv("TOKEN")

    bot = commands.Bot(command_prefix='%')

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user} - {discord.__version__}')
        await bot.change_presence(activity=discord.Game(name="Disc golf"))

    @bot.event
    async def on_message(message):    
        await bot.process_commands(message)

    bot.add_cog(Attachment(bot))
    bot.add_cog(Scores(bot))
    bot.add_cog(Emojis(bot))
    bot.add_cog(Discs(bot))
    bot.add_cog(Bag(bot))

    bot.run(token)

if __name__ == '__main__':
    print ("from __main__")
    main()