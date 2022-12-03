import core.wireless as s
import disnake
import binascii
from io import BytesIO


# Screen shot protocol
async def protocol(self, ctx: disnake.ApplicationCommandInteraction):

    # Make connection with switch and send pixelPeek
    connection = s.connection(self.syscord)
    await connection.connect()
    await connection.switch("pixelPeek")

    # Read the response
    screen = binascii.unhexlify((await connection._r.readline())[:-1])

    # Create an embed and send
    embed = disnake.Embed(color = 0xFFD700)
    embed.set_image(url = "attachment://screen.jpg")
    await ctx.send(file = disnake.File(BytesIO(screen), filename = "screen.jpg"), embed = embed)
