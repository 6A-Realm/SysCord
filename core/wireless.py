from disnake.ext import commands
from yaml import safe_load
import asyncio
from rich.console import Console
console = Console()
from core.addon import *

# Loads switch ip and port from config file
with open("config.yaml") as file:
    data = safe_load(file)
    switchip = data["ip"]
    switchport = data["port"]

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
        except Exception as e: 
            console.print(f"Unable to send commands to switch. {e}", style="red")
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.initiate()

    # Ping switch, fetch title ID, check if auto screen off
    async def initiate(self):
        try:
            self._r, self._w = await asyncio.open_connection(switchip, switchport, limit = 524288)
            console.print(f"Successfully connected to {switchip}:{switchport}.", style="green")

            # Set controller
            await self.switch("detachController")
            await self.switch("controllerType 1")

            # Close socket
            self._w.close()
            await self._w.wait_closed()
            
            for e in cogs:
                try:
                    self.syscord.load_extension("cogs." + e)
                except Exception as err:
                    console.print(f"Unable to load {e} {err}.", style="red")
                    
        except:
            console.print(f"Unable to connect to {switchip}:{switchport}.", style="red")
            console.print("Click here to follow the connection troubleshooting guide: https://github.com/6A-Realm/SysBot.py/wiki/Connection-Issues", style="yellow")

    # IP/Port connection to switch (same thing you would put in sysbot)
    async def connect(self):
        try:
            self._r, self._w = await asyncio.open_connection(switchip, switchport, limit = 1048576)
        except OSError: 
            console.print(f"Unable to connect to {switchip}:{switchport}.", style="red")

def setup(syscord):
    syscord.add_cog(connection(syscord))