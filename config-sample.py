# Required settings (must be changed)
BOT_TOKEN: str = "BOT TOKEN HERE"

# Optional settings (may be changed)
BOT_CMD_PREFIX: str = "^"
BOT_ADMIN_ROLES: list = [
    601467946858184704, # Clan Leader
    458087769303023617, # Clan Director
    679233922885746698, # Chief Operations Officer
    679234440496545792, # Chief Technology Officer
    398544403314245633, # Squad Director
    471757506562228235, # Tarkov Director
    620724284175941663, # Rainbow 6 Siege Director
    674731492647108608, # Post Scriptum Director
    718174200006836415, # Last Oasis Director
]
GIVEAWAY_CHANNEL_ID: int = 569701870839398400 # news-room
GUILD_ID: int = 398543362476605441 # FaT
GIVEAWAY_EMOJI: bytes = b"\xF0\x9F\x8E\x89"  # Unicode emojis only (https://apps.timwhitlock.info/emoji/tables/unicode)
GIVEAWAY_TITLE_EMOJI_ID: int = 410612069398740992  # :FaT:
DATABASE_LOCATION: str = "database.pickle"  # If this file is missing it will be created during startup
WINNERS_MAX_AMOUNT: int = 10000000

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
                f"""```fix\n{BOT_CMD_PREFIX}giveaway [duration] [winners]w"""
                """ [prize]( >[description])```Used to start a giveaway. Insert """
                """the prize, the amount of winners and the duration of the """
                """giveaway. Everything inside the round brackets is optional """
                """(description included).\nThe duration can have """
                """different formats:\n- **+xy** Examples: `+4h`, `+2h 30m`, """
                """`+1d 6h 24m`\n- **M/D/Y  T** Examples: `06/28/20 6pm`, """
                """`12/03/21 7:25 am` """
                f"""```fix\n{BOT_CMD_PREFIX}close [id]```Used to close """
                """a giveaway. Insert the id of the giveaway message to be closed."""
                f"""```fix\n{BOT_CMD_PREFIX}reroll [id] [winners]```Used to """
                """re-roll an amount of winners of a giveaway. Insert the id """
                """of the giveaway message of which one or more winners need """
                """to be re-rolled and the amount of winners to re-roll."""))

TIMEZONE = pytz.timezone("US/Eastern")  # Is used only as a standard timezone for all internal dates. Changing it has no effect.

GIVEAWAY_CHANNEL = None  # defined later during startup

GUILD = None  # defined later during startup

GIVEAWAY_TITLE_EMOJI = None  # defined later during startup
