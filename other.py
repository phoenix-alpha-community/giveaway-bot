"""
This module is used for some other functions and errors used in the bot.py module.
"""

import config
import discord
import re
from discord.ext import commands

# Functions
def is_admin(member: discord.Member):
    """
    Verifies that the member has any of the admin roles.

    Attributes:
        member (discord.Member): The member to be verified.

    Returns:
        None
    """

    # Loop though every role of the member. Set status to True if he has any of the admin roles.
    status = False
    for role in member.roles:
        if role.id in config.BOT_ADMIN_ROLES:
            status = True
            break

    if not status:
        raise discord.ext.commands.MissingAnyRole(
            config.BOT_ADMIN_ROLES)  # Raise MissingAnyRole if the member hasn't any of the admin roles.


def check_giveaway_msg(msg: discord.Message, active: bool, bot: discord.User) -> bool:
    if msg.channel.id != config.GIVEAWAY_CHANNEL.id or msg.author.id != bot:
        return False
    if len(msg.embeds) == 0:
        return False

    pattern = r"([^|]+) \| ([^:]+):$"  # The pattern of the regex.
    status = re.search(pattern, msg.embeds[0].footer).group(2)

    if active:
        if status == "Ends":
            return True
    elif not active:
        if status == "Ended":
            return True

    return False

# Errors
class IncorrectUsageError(commands.CommandError):
    """
    This error gets raised only in the create giveaway function (found in the main file).
    It gets raised when the regex can't define any of the arguments.
    """
    pass

class InexistentMessageError(commands.CommandError):
    """
    This error gets raised only in the reroll function (found in the main file).
    It gets raised when the discord API can't find any message with the given ID
    """
    pass
