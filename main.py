from os import getenv
from dotenv import load_dotenv
import disnake
from disnake.ext import commands


# Read discord bot settings
load_dotenv()
token = getenv("BOT_TOKEN")
owners = getenv("OWNER_IDS")
debug_guilds = getenv("DEBUG_GUILDS")


# Global refistration with debug messages
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

# Define bot
syscord = commands.InteractionBot(
    # SysCord - v.1.2.0
    owner_ids = [int(owners)],
    test_guilds = [int(debug_guilds)],
    command_sync_flags = command_sync_flags,
    intents = disnake.Intents.none()
)

# On ready function in main just in case other files dont load properly
@syscord.event
async def on_ready():
    print(f"[-] {syscord.user.name} has connected to Discord!")

# Initiate a connection and load cogs
syscord.load_extension("core.wireless")

try:
    syscord.run(token)
except Exception as e:
    print(f"Error when logging in: {e}")
