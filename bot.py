"""
Fear and Terror's bot for giveaways on Discord
"""

import config
import discord
import error_handling
from check_roles import is_admin
from database import db_write_ids
from discord.ext import commands
from giveaway import Giveaway, giv_end, draw_winners
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

@bot.command(aliases=["help", "cmd_name"])
async def help_msg(ctx, cmd_name: str = False):
    """
    Sends a help message with description of every available command. Can also send command-specific help messages. These actually return the docs of the function.

    Aliases:
        "help", "info"

    Attributes:
        cmd_name (str): [Optional] The name of the command for which help is needed. An alias works too. If not given, the default help message gets sent.

    Returns:
        None
    """

    is_admin(ctx.author)  # Check if the author is an admin.

    # Check if any command name was given. If not, send the standard help message.
    if not cmd_name:
        await ctx.send(embed=config.HELP_MESSAGE)  # Send the standard help message.

    for command in bot.commands:  # Loop through every command of the bot.
        # Create the embed.
        embed = discord.Embed(
                title=command.name,
                color=discord.Color.gold(),
                description=command.help.replace("\n    ", "\n- ")).set_footer(text="Note: This is the "
                "documentation found in the code for this command. Some info may "
                "not be relevant for you.")

        # Check if the command name is the same as the name of the command for which help is needed.
        if command.name == cmd_name:
            await ctx.send(embed=embed)  # If so, send the embed.
            return
        else:
            #  Check if the name of the command for which help is needed, is an alias of the command.
            for alias in command.aliases:
                if alias == cmd_name:
                    await ctx.send(embed=embed)  # If so, send the embed.
                    return

    # Send the standard help message if the name of the command for which help is needed was not found.
    await ctx.send(embed=config.HELP_MESSAGE)


@bot.command(aliases=["create", "create_giv", "start", "start_giv", "giv",
                      "create_giveaway", "start_giveaway"])
async def giveaway(ctx, winners: int, duration: str, prize: str, *description):
    """
    Summons a giveaway in the giveaway channel.

    Aliases:
        "create", "create_giv", "start", "start_giv", "giv", "create_giveaway", "start_giveaway"

    Attributes:
        winners (int): The amount of winners of the giveaway.
        duration (str): The time before, or at which, the giveaway ends. See the help message for time formats.
        prize (str): The prize of the giveaway.
        description (tuple): [Optional] The description of the giveaway.

    Returns:
        None
    """

    is_admin(ctx.author)  # Check if the author is an admin.

    giv = Giveaway(winners, duration, prize, description, ctx.author)  # Create giveaway object
    await giv.create_giv()  # Start giveaway
    giv.timer_id = delayed_execute(giv_end, [giv.id], giv.duration)  # Start the "timer"
    db_write_ids(giv.id, giv)  # Save the giveaway in the database

@bot.command(aliases=["end", "end_giv", "close_giv", "end_giveaway", "close_giveaway"])
async def close(ctx, msg_id: int):
    """
    Closes the giveaway prematurely.

    Aliases:
        "end", "end_giv", "close_giv", "end_giveaway", "close_giveaway"

    Attributes:
        msg_id (int): The id of the giveaway message of the giveaway to close.

    Returns:
        None
    """

    is_admin(ctx.author)  # Check if the author is an admin.

    await giv_end(msg_id)  # End the giveaway.


@bot.command(aliases=["reroll_giv", "reroll_giveaway"])
async def reroll(ctx, msg_id: int, winners: int = 1):
    """
    Re-draws a specified amount of winners of a giveaway. Also removes the already drawn winners of the giveaway from the "entered" list.

    Aliases:
        "reroll_giv", "reroll_giveaway"

    Attributes:
        msg_id (int): The id of the giveaway message of the giveaway to re-roll.
        winners (int): The amount of winners to re-roll. Default = 1

    Returns:
        None
    """

    is_admin(ctx.author)  # Check if the author is an admin.

    # Check if the number of winners is lower or equal to 0. If it is, raise an error.
    if winners <= 0:
        raise Giveaway.GiveawayWinnersError

    msg: discord.Message = await config.GIVEAWAY_CHANNEL.fetch_message(msg_id)  # Get the message object of the giveaway message.
    new = await draw_winners(msg, winners, reroll=True)  # Draw the new winners. (type: list)

    # Check if the first winner is a member object. If it's not return.
    if new[0] != discord.Member:
        return

    # Format the text for the message
    text = ""
    for member in new:
        text += "\n - " + member.mention
    text_2 = "winners"
    if len(new) == 1:
        text_2 = "winner"

    await ctx.send(f">>> **New {text_2}:**{text}")  # Send the message with the new winners.


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
