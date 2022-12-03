from os import getenv, listdir
from dotenv import load_dotenv
from disnake.ext import commands
import asyncio


# Read Switch settings
load_dotenv()
switchip = getenv("SWITCH_IP")

class connection(commands.Cog):
    def __init__(self, syscord):
        self.syscord = syscord
        self._r = None
        self._w = None

    # sys-botbase to send commands
    async def switch(self, content):
        try:
            content += '\r\n'
            self._w.write(content.encode())
            await self._w.drain()
        except Exception as err: 
            print(f"[!] Unable to send commands to switch. {err}")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.initiate()

    # Ping switch and set controller type
    async def initiate(self):
        try:
            self._r, self._w = await asyncio.open_connection(switchip, 6000, limit = 524288)
            print(f"[✔️] Successfully connected to {switchip}.")

            # Set controller
            await self.switch("configure controllerType 3")

            # Close socket
            self._w.close()
            await self._w.wait_closed()

            # Load cogs
            for extention in listdir("./cogs"):
                if extention.endswith(".py"):
                    try:
                        self.syscord.load_extension("cogs." + extention[:-3])
                        print(f"[✔️] Successfully loaded {extention}.")

                    except Exception as err:
                        print(f"[!] Unable to load {extention} {err}.")

        except Exception as err:
            print(f"[!] Unable to connect to {switchip}:6000. {err}")

            # Attempt to automatically open Connection-Issues wiki page
            try:
                import webbrowser


                url = "https://github.com/6A-Realm/SysBot.py/wiki/Connection-Issues"
                webbrowser.open(url, new = 0, autoraise = True)
            except:
                pass

    # IP/Port connection to switch (same thing you would put in sysbot)
    async def connect(self):
        try:
            self._r, self._w = await asyncio.open_connection(switchip, 6000, limit = 1048576)
        except OSError: 
            print(f"[!] Unable to connect to {switchip}:6000.")

def setup(syscord):
    syscord.add_cog(connection(syscord))
