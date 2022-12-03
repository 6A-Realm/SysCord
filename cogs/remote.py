import core.wireless as s
import disnake
from typing import List, Optional
from disnake.ext import commands
from asyncio import sleep
from core.pixelpeek import protocol


# List of commands
buttons = [
    # Action buttons
    "X", "A", "B", "Y",

    # Split D-Pad
    "DUP", "DRIGHT", "DDOWN", "DLEFT",

    # Dumper buttons
    "L", "R", "ZL", "ZR",
    
    # Others
    "LSTICK", "RSTICK", "PLUS", "MINUS", "HOME", "CAPTURE"

    # Directions
    "UP", "RIGHT", "DOWN", "LEFT"
    ]

directions = {
    "UP": ["yVal 0x7FFF", "yVal 0x0000"], 
    "RIGHT": ["0x7FFF 0x0", "0x0 0x0"], 
    "DOWN": ["yVal -0x8000", "yVal 0x0000"],
    "LEFT": ["-0x8000 0x0", "0x0 0x0"]
}

class remote(commands.Cog):
    def __init__(self, syscord):
        self.syscord = syscord

    async def autocomplete_buttons(ctx, string: str) -> List[str]:
        string = string.lower()
        return [butt for butt in buttons if string in butt.upper()]

# {-- Select, Directional, and Menu Buttons --}
    @commands.slash_command(description = "Automate your Switch")
    @commands.is_owner()
    async def press(self, ctx: disnake.ApplicationCommandInteraction, click: str = commands.Param(autocomplete = autocomplete_buttons), amount: Optional[int] = 1):

        # Create connection with Switch
        connection = s.connection(self.syscord)
        await connection.connect()

        if click in directions:
            for _ in range(amount):
                await connection.switch(f"setStick RIGHT {directions[click][0]}")
                await connection.switch(f"setStick RIGHT {directions[click][1]}")
        else:
            for _ in range(amount):
                await connection.switch(f"click {click}")

        # Wait to prevent taking images of moving screen
        await sleep(1.0)
        await protocol(self, ctx)


def setup(syscord):
    syscord.add_cog(remote(syscord))
