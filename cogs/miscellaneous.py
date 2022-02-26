import core.wireless as s
import asyncio
from disnake.ext import commands

class miscellaneous(commands.Cog):
    def __init__(self, syscord):
        self.syscord = syscord

# {-- Other SBB Related Commands --}
    @commands.command()
    @commands.is_owner()
    async def newcontroller(self, ctx):
        connection = s.connection(self.syscord)
        await connection.connect()
        await connection.switch("detachController")
        await asyncio.sleep(0.5)
        await connection.switch("controllerType 1")
        await ctx.send("Your controller was reset.")

    @commands.command()
    @commands.is_owner()
    async def titleid(self, ctx): 
        connection = s.connection(self.syscord)
        await connection.connect()
        await connection.switch("getTitleID")
        title = ((await connection._r.read(689))[:-1]).decode("utf-8")
        await ctx.send(title)

            
def setup(syscord):
    syscord.add_cog(miscellaneous(syscord))