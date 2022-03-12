from disnake.ext import commands
from yaml import safe_load
import asyncio
from rich.console import Console
console = Console()

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

    # IP/Port connection to switch (same thing you would put in sysbot)
    async def connect(self):
        try:
            self._r, self._w = await asyncio.open_connection(switchip, switchport, limit = 1048576)
        except OSError: 
            console.print(f"Unable to connect to {switchip}:{switchport}.", style="red")

def setup(syscord):
    syscord.add_cog(connection(syscord))