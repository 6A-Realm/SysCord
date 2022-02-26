# Imports 
import disnake
from disnake.ext import commands
from yaml import load, warnings
import core.wireless as s

# Load config.yaml
with open("config.yaml") as file:
    data = load(file)
    token = data["token"]
    botprefix = data["prefix"]

# Defining the bot and settings
syscord = commands.Bot(name="SysCord - V.0.1.0", command_prefix = botprefix, help_command = None, activity = disnake.Game(name="SysCord"), intents = disnake.Intents.all())
warnings({'YAMLLoadWarning': False})

# Connect and initiate connection
syscord.load_extension("core.wireless")
s.connection(syscord).initiate()

try:
    syscord.run(token)
    print(f"Logged into {syscord.name}")
except Exception as e:
    print(f"Error when logging in: {e}")