import os
import logging

import discord
from discord.ext import commands 
from cogs.musicCog import MusicCog
from cogs.errorCog import ErrorCog
from cogs.otherCog import CommandsCog

# log error output to file
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#loading env variables from heroku

TOKEN = os.getenv('BOT_TOKEN')

#need intents explicitly enabled for updated discord api
intents = discord.Intents.all()

#creating the bot using the extension
bot = commands.Bot(command_prefix='-', intents=intents)

# adds command functionality from cogs.py
bot.add_cog(MusicCog(bot))
bot.add_cog(CommandsCog(bot))
# REMEMBER TO UNCOMMENT THIS
bot.add_cog(ErrorCog(bot))

# runs, token passed to function as the bot account
bot.run(TOKEN)
