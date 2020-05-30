# Required settings (must be changed)
BOT_TOKEN: str = "BOT TOKEN HERE"

# Optional settings (may be changed)
BOT_CMD_PREFIX: str = "^"
BOT_ADMIN_ROLES: [int, list] = 677916986352730112  # Test role id, must be changed
GIVEAWAY_CHANNEL_ID: int = 643985296668622848  # Test channel id, must be changed
GUILD_ID: int = 643983215056519178  # Test server id, must be changed
GIVEAWAY_EMOJI: str = b"\xF0\x9F\x8E\x89"  # unicode emojis only (https://apps.timwhitlock.info/emoji/tables/unicode)
DATABASE_LOCATION: str = "database.pickle"

###############################################################################
# DO NOT EDIT BELOW
###############################################################################
import discord
import pytz

SCHEDULER_DB_FILENAME = "scheduler-db.sqlite"

HELP_MESSAGE = discord.Embed(
    title="Help",
    color=discord.Color.gold(),
    description=(f"""```fix\n{BOT_CMD_PREFIX}giveaway [winners] [duration]"""
                 """ [prize]```Used to start a giveaway. Insert the """
                 """prize, the amount of winners and the duration of the giveaway."""
                 """The duration can have different formats:\n- **+xy** """
                 """Examples: `"+4h"`, `"+2h 30m"`, `"+1d 6h 24m"`\n- **M/D/Y   T** """
                 """Examples: `"06/28/20 6pm"`, `"12/03/21 7:25 am"`\nPlease mind the double quotes.""")
)

TIMEZONE = pytz.timezone("US/Eastern")

GIVEAWAY_CHANNEL = None  # defined later after startup, bot.py

GUILD = None  # defined later after startup, bot.py
