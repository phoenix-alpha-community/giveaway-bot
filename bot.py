"""
Fear and Terror's bot for giveaways on Discord
"""

import config
import discord
import error_handling
from database import db_write_ids
from discord.ext import commands
from giveaway import Giveaway, giv_end
from scheduling import init_scheduler, delayed_execute

bot = commands.Bot(command_prefix=config.BOT_CMD_PREFIX, help_command=None)


###############################################################################
# Events
###############################################################################

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    init_scheduler()
    await init()
    print('------')


@bot.event
async def on_command_error(ctx, error):
    await error_handling.handle_error(ctx, error)


###############################################################################
# Commands
###############################################################################

@bot.command(aliases=["help"])
async def help_msg(ctx):
    """
    Sends a help message with description of every available command.

    Attributes:
        None

    Returns:
        None
    """

    await ctx.send(embed=config.HELP_MESSAGE)  # Send the help message


@bot.command()
@commands.has_role(config.BOT_ADMIN_ROLES)
async def giveaway(ctx, winners: int, duration: str, prize: str, *description):
    """
    Summons a giveaway in the giveaway channel.

    Attributes:
        winners (int): The amount of winners of the giveaway.
        duration (str): The time before, or at which, the giveaway ends.
                        See the help message for time formats.
        prize (str): The prize of the giveaway.
        description (tuple): [Optional] The description of the giveaway.

    Returns:
        None
    """

    giv = Giveaway(winners, duration, prize, description, ctx.author)  # Create giveaway object
    await giv.create_giv()  # Start giveaway
    db_write_ids(giv.id, giv)  # Save the giveaway in the database
    delayed_execute(giv_end, [giv.id], giv.duration)  # Start the "timer"


###############################################################################
# Startup
###############################################################################

async def init():
    """
    Executes a series of actions to set-up the bot.

    Attributes:
        None

    Returns:
        None
    """

    config.GUILD = bot.get_guild(config.GUILD_ID)  # Get guild object
    config.GIVEAWAY_CHANNEL = config.GUILD.get_channel(config.GIVEAWAY_CHANNEL_ID)  # Get giveaway channel object

    await bot.change_presence(activity=discord.Game(f"FaT | {config.BOT_CMD_PREFIX}help"))  # Change bot's activity

    # Check if database file is present. If not, create it.
    try:
        with open(config.DATABASE_LOCATION):
            pass
    except FileNotFoundError:
        with open(config.DATABASE_LOCATION, "w"):
            pass

    print("Initial set-up completed")


if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)
