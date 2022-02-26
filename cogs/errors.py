import disnake
from disnake.ext import commands
from disnake.ext.commands import CommandNotFound

class ERRORS(commands.Cog):
    def __init__(self, syscord):
        self.syscord = syscord

    # Error Handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            pass
        elif isinstance(error, disnake.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("You are missing required arguments.")
        elif isinstance(error, disnake.ext.commands.errors.BadArgument):
            await ctx.send("You were unclear with your arguments.")
        elif isinstance(error, commands.NotOwner):
            await ctx.send("This is an owner only command.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"I'm missing the following permissions: \n**{', '.join(error.missing_permissions)}**")
        else:
            print(f"Logical error found {error}")


def setup(syscord):
        syscord.add_cog(ERRORS(syscord))