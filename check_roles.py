"""
This module is used to check the roles of a discord member.
"""

import config
import discord

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
