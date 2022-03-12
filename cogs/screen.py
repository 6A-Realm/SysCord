import core.wireless as s
import disnake, asyncio, typing
from disnake.ext import commands
from core.pixelpeek import protocol

class screen(commands.Cog):
    def __init__(self, syscord):
        self.syscord = syscord
        
    # {-- Screen Settings --}
    @commands.command()
    @commands.is_owner()
    async def screen(self, ctx, function = None, delay: typing.Optional[int] = 60):
        embed=disnake.Embed(title="Nintendo Switch Manual Screen Control", description="Bot owners and sudo members can control their connected Nintendo Switch screen on {switchip}:{switchport} using the following commands.", color=0x17c70a)
        embed.add_field(name="Screen Commands:", value="`on, off, shot, capture, percent`", inline=False)
        embed.set_footer(text="Capture does not work for LGPE.")
        if function is None:
            await ctx.send(embed = embed)
        check = function.lower()
        connection = s.connection(self.syscord)
        await connection.connect()
        if check == "off":
            await connection.switch("screenOff")
            await ctx.send("Your switch screen was turned `off`.")
        elif check == "on":
            await connection.switch("screenOn")
            await ctx.send("Your switch screen was turned `on`.")
        elif check == "delay":
            await connection.switch("screenOn")
            await ctx.send(f"Your switch screen was turned `on`. It will turn off in `{delay}` seconds.")
            await asyncio.sleep(delay)
            await connection.switch("screenOff")
            await ctx.send(f"Your switch screen was turned `off`.")
        elif check == "shot":
            await protocol(ctx)
        elif check == "capture":
            await connection.switch("click CAPTURE")
            embed=disnake.Embed(description="Your switch screen was attempted to be captured.", color=0x17c70a)
            embed.set_footer(text="Note that this function does not work for LGPE.")
            await ctx.send(embed = embed)
        elif check in ["battery", "percent"]:
            await connection.switch("charge")
            charge = ((await connection._r.read(689))[:-1]).decode("utf-8")
            await ctx.send(f"Your Switch's battery level is at {str(charge)}%.")
        else:
            await ctx.send(embed = embed)

            
def setup(syscord):
    syscord.add_cog(screen(syscord))