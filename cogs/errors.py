from disnake.ext import commands

class err(commands.Cog):
    def __init__(self, syscord):
        self.syscord = syscord

    # Error Handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You are missing required arguments.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("You were unclear with your arguments.")
        elif isinstance(error, commands.NotOwner):
            await ctx.send("Only the owner of this bot can use this command.")
        else:
            print(f"Logical error found {error}")

def setup(syscord):
    syscord.add_cog(err(syscord))