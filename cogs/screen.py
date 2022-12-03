import core.wireless as s
from typing import List, Optional
import disnake
import asyncio
from disnake.ext import commands
from core.pixelpeek import protocol

functions = ["off", "on", "delay", "battery"]

class screen(commands.Cog):
    def __init__(self, syscord):
        self.syscord = syscord

    async def autocomplete_functions(ctx, string: str) -> List[str]:
        string = string.lower()
        return [func for func in functions if string in func.lower()]

    # {-- Screen Settings --}
    @commands.slash_command(description = "Control your Switch screen")
    @commands.is_owner()
    async def screen(self, ctx: disnake.ApplicationCommandInteraction, function: str = commands.Param(autocomplete = autocomplete_functions), delay: Optional[int] = 60):

        connection = s.connection(self.syscord)
        await connection.connect()
        if function == "off":
            await connection.switch("screenOff")
            await ctx.send("Your switch screen was turned `off`.")
        elif function == "on":
            await connection.switch("screenOn")
            await ctx.send("Your switch screen was turned `on`.")
        elif function == "delay":
            await connection.switch("screenOn")
            await ctx.send(f"Your switch screen was turned `on`. It will turn off in `{delay}` seconds.")
            await asyncio.sleep(delay)
            await connection.switch("screenOff")
            await ctx.send(f"Your switch screen was turned `off`.")
        elif function == "battery":
            await connection.switch("charge")
            charge = ((await connection._r.read(689))[:-1]).decode("utf-8")
            await ctx.send(f"Your Switch's battery level is at {str(charge)}%.")
        else:
            await ctx.send(embed = embed)


def setup(syscord):
    syscord.add_cog(screen(syscord))