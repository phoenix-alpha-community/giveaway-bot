from config import HELP_MESSAGE
import traceback
from discord.ext import commands
from giveaway import Giveaway

async def handle_error(ctx: commands.Context,
                       error: commands.CommandError) -> None:
    '''
    Global error handler.
    Responds to CommandErrors with appropriate messages in the Discord channel
    in which the command was used.
    This error handler should be called from `bot.on_command_error`.
    '''

    # Syntax errors
    syntax_error_classes = [
        commands.MissingRequiredArgument,
        commands.errors.BadArgument
    ]
    for cls in syntax_error_classes:
        if isinstance(error, cls):
            await ctx.send(f"> {ctx.author.mention} Incorrect usage. "
                     f"See usage help below.")
            await ctx.send(embed=HELP_MESSAGE)
            return

    # Costume errors
    if isinstance(error, Giveaway.GiveawayWinnersError):
        await ctx.send(f"> {ctx.author.mention} Winners amount is too low.")

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

    # Internal errors
    if isinstance(error, Giveaway.GiveawayChannelError):
        await ctx.send(f"> {ctx.author.mention} An internal error has occurred."
                       "Please contact the programming team and tell them about it.")
        return

    # Unknown command
    if isinstance(error, commands.CommandNotFound):
        return  # ignore

    # Default catch-all
    await ctx.send(f"> {ctx.author.mention} An unknown error occurred. "
             f"Please contact the programming team and tell them what you did "
             f"to produce this error.")
    traceback.print_exception(type(error), error, error.__traceback__)
