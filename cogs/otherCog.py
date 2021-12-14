###############################################################################################
# cog that contains commands unrelated to music
# if you wish to add more commands, house them here
###############################################################################################

from discord.ext import commands
from misc.helptext import helpText


class CommandsCog(commands.Cog, name='Commands'):
    # attributes
    def __init__(self, bot: commands.bot):
        self.bot = bot

    ############################################################################################### 
    # async below
    ###############################################################################################
    
    # posts a gif of a pug dancing
    @commands.command(brief=helpText['danceBrief'], description=helpText['danceDesc'], aliases=['groove'])        
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dance(self, ctx):
        # you can paste any dancing gif you like here. Make sure it stays within those two quotes inside the parentheses
        await ctx.send('https://c.tenor.com/j3kOOpQzhpoAAAAM/doge-dance.gif')

    # gives randomized advice from wisdom.py, easter egg
    # those who wish to customize the advice, alter the strings inside wisdom.py
    @commands.command(brief=helpText['wisdomBrief'], description=helpText['wisdomDesc'], aliases=['advice'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def wisdom(self, ctx):
        import random
        from misc.wisdom import wisdom
        await ctx.send(random.choice(wisdom))
