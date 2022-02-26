import core.wireless as s
import disnake, asyncio, typing
from disnake.ext import commands
from core.pixelpeek import protocol

class remote(commands.Cog):
    def __init__(self, syscord):
        self.syscord = syscord

# {-- Select, Directional, and Menu Buttons --}
    @commands.command()
    @commands.is_owner()
    async def press(self, ctx, value = None, amount: typing.Optional[int] = 1):

        # Default embed
        embed=disnake.Embed(title="Nintendo Switch Manual Control", description="Bot owners and sudo members can remote control their connected Nintendo Switch on {switchip}:{switchport} using the following commands.", color=0x17c70a)
        embed.add_field(name="Select Buttons:", value="`x, a, b, y`", inline=False)
        embed.add_field(name="Directional Buttons:", value="`up, right, down, left`", inline=False)
        embed.add_field(name="Other Commands:", value="`inject, dump, home, plus min`", inline=False)
        embed.set_footer(text="Minus does not work for LGPE.")
        if value is None: 
            await ctx.send(embed=embed)

        # List of commands
        singles = ["X", "A", "B", "Y", "PLUS", "MINUS", "HOME", "CAPTURE"]

        # Create connection with Switch
        connection = s.connection(self.syscord)
        await connection.connect()

        # Convert to uppercase and do functions
        check = value.upper()
        if check in singles:
                for x in range(amount):
                    await connection.switch(f"click {check}")
                    await asyncio.sleep(0.5)
                await protocol(self, ctx)
        elif check == "UP":
            for up in range(amount):
                await connection.switch("setStick RIGHT yVal 0x7FFF")
                await connection.switch("setStick RIGHT yVal 0x0000")
                await asyncio.sleep(0.5)
            await protocol(self, ctx)
        elif check == "RIGHT":
            for right in range(amount):
                await connection.switch("setStick RIGHT 0x7FFF 0x0")
                await connection.switch("setStick RIGHT 0x0 0x0")
                await asyncio.sleep(0.5)
            await protocol(self, ctx)
        elif check == "DOWN":
            for down in range(amount):
                await connection.switch("setStick RIGHT yVal -0x8000")
                await connection.switch("setStick RIGHT yVal 0x0000")
                await asyncio.sleep(0.5)
            await protocol(self, ctx)
        elif check == "LEFT":
            for left in range(amount):
                await connection.switch("setStick RIGHT -0x8000 0x0")
                await connection.switch("setStick RIGHT 0x0 0x0")
            await protocol(self, ctx) 
        else:
            await ctx.send(embed=embed)


def setup(syscord):
    syscord.add_cog(remote(syscord))