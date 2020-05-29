'''
Fear and Terror's bot for giveaways on Discord
'''

import config
from database import db_write_ids
import discord
from discord.ext import commands
from error_handling import handle_error
from giveaway import Giveaway

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


@bot.event
async def on_command_error(ctx, error):
    await handle_error(ctx, error)


###############################################################################
# Commands
###############################################################################

@bot.command(aliases=["help"])
async def help_msg(ctx):
    await ctx.send(embed=config.HELP_MESSAGE)


@bot.command()
@commands.has_role(config.BOT_ADMIN_ROLES)
async def giveaway(ctx, winners: int, duration: str, prize: str):
    giv = Giveaway(winners, duration, prize, ctx.author)
    await giv.create_giv(ctx)
    db_write_ids(giv.id, giv)


###############################################################################
# Startup
###############################################################################

def init():
    config.GUILD = bot.get_guild(config.GUILD_ID)
    config.GIVEAWAY_CHANNEL = await config.GUILD.get_channel(config.GIVEAWAY_CHANNEL_ID)


if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)
    init()
