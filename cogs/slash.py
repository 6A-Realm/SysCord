import disnake, binascii
import core.wireless as s
from disnake.ext import commands
from io import BytesIO

class slash(commands.Cog):
    def __init__(self, syscord):
        self.syscord = syscord
        
    @commands.slash_command(description = "Sends a picture of your switch screen")
    async def peek(self, ctx):
        connection = s.connection(self.syscord)
        await connection.connect()
        await connection.switch("pixelPeek")
        screen = binascii.unhexlify((await connection._r.readline())[:-1])
        embed = disnake.Embed(color=0xFFD700)
        embed.set_image(url="attachment://screen.jpg")
        await ctx.send(file = disnake.File(BytesIO(screen), filename="screen.jpg"), embed = embed)

def setup(syscord):
    syscord.add_cog(slash(syscord))            