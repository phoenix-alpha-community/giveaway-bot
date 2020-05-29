import config
import discord
import pytimeparse
from datetime import datetime, timedelta
from dateutil import parser
from discord.ext import commands

class Giveaway:
    def __init__(self, winners: int, duration: str, prize: str,
                 host: discord.Member):
        if winners <= 0:
            raise self.GiveawayWinnersError

        self.duration = self.dur_trnsl(duration)
        self.host = host.id
        self.id = None  # defined after __init__() in create_giv
        self.prize = prize
        self.winners = winners

    # Internal functions: primary purpose
    async def create_giv(self, ctx: commands.Context) -> None:
        win = "winners"
        if self.winners == 1:
            win = "winner"

        if config.GIVEAWAY_CHANNEL is None:
            await self.get_channel(ctx)

        self.id = (await config.GIVEAWAY_CHANNEL.send(":FaT: **GIVEAWAY** :FaT:",
        embed=discord.Embed(
            color=discord.Color.green(),
            title=self.prize,
            timestamp=self.duration,
            description=f"Click the reaction below to enter!\nHosted "
                        f"by: <@{self.host}>"
        ).set_footer(text=f"{str(self.winners)} {win} | Ends at:"))).id

    async def end_giv(self):
        pass

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

    async def get_member(self) -> discord.Member:
        return await config.GUILD.get_member(self.host)

    async def get_message(self) -> discord.Message:
        return await config.GIVEAWAY_CHANNEL.get_message(self.id)

    # Errors
    class GiveawayWinnersError(commands.CommandError):
        pass

    class GiveawayChannelError(commands.CommandError):
        pass
