from disnake.ext import commands, tasks
import disnake
import random


class PresenceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.presence.start()

    # Create a async loop
    @tasks.loop(minutes = 2)
    async def presence(self):
        await self.bot.wait_until_ready()

        # Flip through presense
        presence = await self.random_text()
        await self.bot.change_presence(
            activity = disnake.Activity(
                type = disnake.ActivityType.playing,
                name = presence
            )
        )

    # Generate random presense text
    async def random_text(self):
        presence_list = [
            "/ commands only",
            "SysCord - by 6A",
            "https://github.com/6A-Realm/SysCord",
        ]

        return random.choice(presence_list)


def setup(bot):
    bot.add_cog(PresenceCog(bot))
