# Imports 
import disnake, asyncio
from disnake.ext import commands
from yaml import safe_load
from rich.console import Console
console = Console()

# Load config.yaml
with open("config.yaml") as file:
    data = safe_load(file)
    token = data["token"]
    botprefix = data["prefix"]
    switchip = data["ip"]
    switchport = data["port"]

# Defining the bot and settings
syscord = commands.Bot(name="SysCord - V.1.0.0", command_prefix = botprefix, help_command = None, activity = disnake.Game(name="SysCord"), intents = disnake.Intents.all())

# Ping switch, set controller, load cogs
async def initiate(syscord):

    # List of cogs
    cogs = str["error", "image", "miscellaneous", "remote", "screen"]

    try:
        reader, writer = await asyncio.open_connection(switchip, switchport)
        console.print(f"Successfully connected to {switchip}:{switchport}.", style="green")

        # Set controller
        try:
            await writer.write("detachController\r\n".encode())
            await writer.drain()
        except:
            print("1")
        try:
            await writer.write("controllerType 1\r\n".encode())
            await writer.drain()
        except:
            print("2")

        try:
            # Close socket connection
            writer.close()
            await writer.wait_closed()
        except:
            print("3")

        try:
            # Load cogs
            for e in cogs:
                try:
                    syscord.load_extension("cogs." + cogs)
                except Exception as err:
                    console.print(f"Unable to load {e} {err}.", style="red")
        except:
            print("4")
    except:
        console.print(f"Unable to connect to {switchip}:{switchport}.", style="red")
        console.print("Click here to follow the connection troubleshooting guide: https://github.com/6A-Realm/SysBot.py/wiki/Connection-Issues", style="yellow")

#Debugger
syscord.load_extension('jishaku')

# Start all
asyncio.run(initiate(syscord))

try:
    syscord.run(token)
    print(f"Logged into {syscord.name}")
except Exception as e:
    print(f"Error when logging in: {e}")