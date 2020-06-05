# Required settings (must be changed)
BOT_TOKEN: str = "BOT TOKEN HERE"

# Optional settings (may be changed)
BOT_CMD_PREFIX: str = "^"
BOT_ADMIN_ROLES: list = [677916986352730112]  # Test role id, must be changed
GIVEAWAY_CHANNEL_ID: int = 643985296668622848  # Test channel id, must be changed
GUILD_ID: int = 643983215056519178  # Test server id, must be changed
GIVEAWAY_EMOJI: bytes = b"\xF0\x9F\x8E\x89"  # Unicode emojis only (https://apps.timwhitlock.info/emoji/tables/unicode)
DATABASE_LOCATION: str = "database.pickle"  # If this file is missing it will be created during startup

###############################################################################
# DO NOT EDIT BELOW
###############################################################################
import discord
import pytz

SCHEDULER_DB_FILENAME = "scheduler-db.sqlite"

HELP_MESSAGE = discord.Embed(
    title="Help",
    color=discord.Color.gold(),
    description=(f"""```fix\n{BOT_CMD_PREFIX}help [command_name]``` Give """
                """the name of the command for which help is needed. An alias """
                """works too. If no name is given (or the given command is """
                """not found), this message gets sent."""
                f"""```fix\n{BOT_CMD_PREFIX}giveaway [winners] [duration]"""
                """ "[prize]" [description]```Used to start a giveaway. Insert """
                """the prize, the amount of winners and the duration of the """
                """giveaway. The description is optional.\nThe duration can have """
                """different formats:\n- **+xy** Examples: `+4h`, `"+2h 30m"`, """
                """`"+1d 6h 24m"`\n- **M/D/Y  T** Examples: `"06/28/20 6pm"`, """
                """`"12/03/21 7:25 am"`\nPlease mind all double quote."""
                f"""```fix\n{BOT_CMD_PREFIX}close [id]```Used to close """
                """a giveaway. Insert the id of the giveaway message to be closed."""
                f"""```fix\n{BOT_CMD_PREFIX}reroll [id] [winners]```Used to """
                """reroll an amount of winners of a giveaway. Insert the id """
                """of the giveaway message of which one or more winners need """
                """to be rerolled and the amount of winners to reroll."""))

TIMEZONE = pytz.timezone("US/Eastern")  # Is used only as a standard timezone for all internal dates. Changing it has no effect.

GIVEAWAY_CHANNEL = None  # defined later during startup

GUILD = None  # defined later during startup
