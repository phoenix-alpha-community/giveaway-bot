import config
import discord
import pytimeparse
from datetime import datetime, timedelta
from dateutil import parser
from discord.ext import commands

class Giveaway:
    def __init__(self, winners: int, duration: str, prize: str,
                 host: discord.User):
        if winners <= 0:
            raise self.GiveawayWinnersError

        self.channel = None  # defined after __init__() in create_giv
        self.duration = self.dur_trnsl(duration)
        self.host = host
        self.id = None  # defined after __init__() in create_giv
        self.prize = prize
        self.winners = winners

    # Internal functions: primary purpose
    async def create_giv(self, ctx: commands.Context) -> None:
        win = "winners"
        if self.winners == 1:
            win = "winner"

        if self.channel is None:
            await self.fetch_channel(ctx)

        self.id = (await self.channel.send(":FaT: **GIVEAWAY** :FaT:",
        embed=discord.Embed(
            color=discord.Color.green(),
            title=self.prize,
            timestamp=self.duration,
            description=f"Click the reaction below to enter!\nHosted "
                        f"by: {self.host.mention}"
        ).set_footer(text=f"{str(self.winners)} {win} | Ends at:"))).id

    # Internal functions: secondary purpose
    def dur_trnsl(self, dur) -> datetime:
        def _add():
            if not dur.startswith("+"):
                return False

            dt = datetime.now(config.TIMEZONE)
            delta = timedelta(seconds=pytimeparse.parse(dur[1:].lower()))

            return dt + delta

        time = _add()
        if not time:
            return config.TIMEZONE.localize(parser.parse(dur))
        return time.replace(second=0, microsecond=0)

    async def fetch_channel(self, ctx: commands.Context) -> None:
        giv_channel = None
        for channel in await ctx.guild.fetch_channels():
            if channel.id == config.GIVEAWAY_CHANNEL:
                giv_channel = channel
                break
        if giv_channel is None:
            raise self.GiveawayChannelError

        Giveaway.channel = giv_channel
        self.channel = giv_channel

    # Errors
    class GiveawayWinnersError(commands.CommandError):
        pass

    class GiveawayChannelError(commands.CommandError):
        pass
