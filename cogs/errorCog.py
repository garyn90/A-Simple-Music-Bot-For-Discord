###############################################################################################
# cog for error handling, global listening 
###############################################################################################


from discord.ext import commands
from misc.messages import messages


class ErrorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # global error handling, listening for commands inside all cogs, rather than command specific error handling
    @commands.Cog.listener() 
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(messages['Cooldown'])
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(messages['cmdNotFound'])
        else:
            #NOTE (so you don't tear your hair out again): Keep this commented out EXCEPT for when: diagnosing errors that slip past LOCALIZED ERROR HANDLING)
            raise error
            #pass
    # mandatory setup for adding this cog to bot 
    def setup(self, bot):
        bot.add_cog(ErrorCog(bot))
