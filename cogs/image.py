import core.wireless as s
import disnake
import binascii
import aiofiles
from disnake.ext import commands
from io import BytesIO
from datetime import datetime
from core.pixelpeek import protocol


class image(commands.Cog):
    def __init__(self, syscord):
        self.syscord = syscord

# {-- Photo Management Commands --} 
    @commands.slash_command(description = "Send a picture of Switch screen")
    @commands.is_owner()
    async def peek(self, ctx: disnake.ApplicationCommandInteraction):
        await protocol(self, ctx)

    @commands.slash_command(description = "Save screenshot to PC")
    @commands.is_owner()
    async def screenshot(self, ctx: disnake.ApplicationCommandInteraction):
        connection = s.connection(self.syscord)
        await connection.connect()
        await connection.switch("pixelPeek")
        screen = binascii.unhexlify((await connection._r.readline())[:-1])

        # Get time and date
        timestamp = datetime.now().strftime("%d-%m-%Y %H-%M-%S")

        # Create a file and save to album
        async with aiofiles.open(f"album/{timestamp}.jpg", "wb+") as f:
            await f.write(screen)
            
        # Send as embed
        embed = disnake.Embed(title = f"Screenshot of {ctx.author.name}'s Switch", color = ctx.author.color)
        embed.set_image(url = "attachment://screen.jpg")
        
        # Footer timestamp
        index = timestamp.find(" ")
        textstamp = timestamp[:index] + "\nTime: " + timestamp[index:]
        embed.set_footer(text = f"Date: {textstamp}")

        await ctx.send(file = disnake.File(BytesIO(screen), filename = "screen.jpg"), embed = embed)


def setup(syscord):
    syscord.add_cog(image(syscord))
