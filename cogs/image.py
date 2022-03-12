import core.wireless as s
import disnake, binascii, aiofiles
from disnake.ext import commands
from io import BytesIO
from datetime import datetime

class image(commands.Cog):
    def __init__(self, syscord):
        self.syscord = syscord

# {-- Photo Management Commands --} 
    @commands.command(allias = ["pixelpeek", "screengrab"])
    @commands.is_owner()
    async def peek(self, ctx):
        connection = s.connection(self.syscord)
        await connection.connect()
        await connection.switch("pixelPeek")
        screen = binascii.unhexlify((await connection._r.readline())[:-1])
        embed = disnake.Embed(color=0xFFD700)
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file = disnake.File(BytesIO(screen), filename="screen.jpg"), embed = embed)

    @commands.command()
    async def screenshot(self, ctx): 
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
        embed.set_image(url="attachment://screen.jpg")
        
        # Footer timestamp
        index = timestamp.find(" ")
        textstamp = timestamp[:index] + "\nTime: " + timestamp[index:]
        embed.set_footer(text = f"Date: {textstamp}")

        await ctx.send(file = disnake.File(BytesIO(screen), filename="screen.jpg"), embed = embed)
        

def setup(syscord):
    syscord.add_cog(image(syscord))