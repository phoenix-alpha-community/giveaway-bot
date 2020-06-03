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
    """

    await ctx.send(embed=config.HELP_MESSAGE)


@bot.command()
@commands.has_role(config.BOT_ADMIN_ROLES)
async def giveaway(ctx, winners: int, duration: str, prize: str, *description):
    """
    Creates a giveaway in the giveaway channel.

    Attributes:
        winners (int): The amount of winners of the giveaway.
        duration (str): The time before, or at which, the giveaway ends.
                        See the help message for time formats.
        prize (str): The prize of the giveaway.
        description (str): [Optional] The description of the giveaway.
    """

    giv = Giveaway(winners, duration, prize, description, ctx.author)
    await giv.create_giv()
    db_write_ids(giv.id, giv)
    delayed_execute(giv_end, [giv.id], giv.duration)


###############################################################################
# Startup
###############################################################################

async def init():
    config.GUILD = bot.get_guild(config.GUILD_ID)
    config.GIVEAWAY_CHANNEL = config.GUILD.get_channel(config.GIVEAWAY_CHANNEL_ID)
    await bot.change_presence(activity=discord.Game(f"FaT | {config.BOT_CMD_PREFIX}help"))

    try:
        with open(config.DATABASE_LOCATION):
            pass
    except FileNotFoundError:
        with open(config.DATABASE_LOCATION, "w"):
            pass

    print("Initial set-up completed")


if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)
