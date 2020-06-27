import discord
import other
import traceback
from config import HELP_MESSAGE, WINNERS_MAX_AMOUNT
from discord.ext import commands
from giveaway import Giveaway

async def handle_error(ctx: commands.Context,
                       error: commands.CommandError) -> None:
    """
    Global error handler.
    Responds to CommandErrors with appropriate messages in the Discord channel
    in which the command was used.
    This error handler should be called from `bot.on_command_error`.
    """

    # Syntax errors
    syntax_error_classes = [
        commands.MissingRequiredArgument,
        commands.errors.BadArgument,
        other.IncorrectUsageError
    ]
    for cls in syntax_error_classes:
        if isinstance(error, cls):
            await ctx.send(f"> {ctx.author.mention} The command format you used is incorrect. "
                     f"See correct usage for the command in the help message below.")
            await ctx.send(embed=HELP_MESSAGE)
            return

    # Costume errors
    if isinstance(error, Giveaway.GiveawayLowWinnersError):
        await ctx.send(f"> {ctx.author.mention} Winners amount is too low.")
        return

    if isinstance(error, Giveaway.GiveawayHighWinnersError):
        await ctx.send(f"> {ctx.author.mention} Winners amount is too high. "
                       f"(MAX = {WINNERS_MAX_AMOUNT})")
        return

    if isinstance(error, Giveaway.GiveawayPastDateError):
        await ctx.send(f"{ctx.author.mention} Time machines don't exist yet.")
        return

    if isinstance(error, Giveaway.GiveawayFutureDateError):
        await ctx.send(f"{ctx.author.mention} The end of the giveaway is "
                       f"more than 365 days away (1 year).\nSet it closer.")
        return

    if isinstance(error, Giveaway.GiveawayInvalidDuration):
        await ctx.send(f"{ctx.author.mention} An invalid duration was given.\n"
                       f"Read the help message for example-formats.")
        return

    if isinstance(error, other.InexistentMessageError):
        await ctx.send(f"{ctx.author.mention} The given ID doesn't match any "
                       "of the giveaway messages. This could also happen if "
                       "the giveaway message has been deleted.")
        return

    # Permission errors
    if isinstance(error, commands.MissingRole) \
            or isinstance(error, commands.MissingAnyRole):
        await ctx.send(f"> {ctx.author.mention} You do not have the role(s) "
                       f"required to use this command.")
        return

    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"> {ctx.author.mention} Command is not applicable or "
                       f"you lack the permission to use it.")
        return

    if isinstance(error, discord.errors.Forbidden):
        await ctx.send((f"> {ctx.author.mention} The bot is not allowed in "
                        f"the giveaway channel."))

    # Unknown command
    if isinstance(error, commands.CommandNotFound):
        return  # ignore

    # Default catch-all
    await ctx.send(f"> {ctx.author.mention} An unknown error occurred. "
             f"Please contact the programming team and tell them what you did "
             f"to produce this error.")
    traceback.print_exception(type(error), error, error.__traceback__)
