# Imports 
import disnake
from disnake.ext import commands
from yaml import safe_load

# Load config.yaml
with open("config.yaml") as file:
    data = safe_load(file)
    token = data["token"]
    botprefix = data["prefix"]

# Defining the bot and settings
syscord = commands.Bot(name="SysCord - V.1.1.0", command_prefix = botprefix, help_command = None, activity = disnake.Game(name="SysCord"), intents = disnake.Intents.all())
syscord.load_extension("core.wireless")
syscord.load_extension("jishaku")

try:
    syscord.run(token)
    print(f"Logged into {syscord.name}")
except Exception as e:
    print(f"Error when logging in: {e}")