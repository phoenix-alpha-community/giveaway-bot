import config
import discord
import pytimeparse
from database import db_read_ids, db_remove_ids
from datetime import datetime, timedelta
from dateutil import parser
from discord.ext import commands
from random import randrange


class Giveaway:
    def __init__(self, winners: int, duration: str, prize: str,
                 description, host: discord.Member):
        if winners <= 0:
            raise self.GiveawayWinnersError

        self.duration = self.dur_trnsl(duration)
        self.description = self.format_desc(description)
        self.host = host.id
        self.id = None  # defined after __init__() in create_giv
        self.prize = prize
        self.winners = winners

    # Internal functions: primary purpose
    async def create_giv(self) -> None:
        win = "winners"
        if self.winners == 1:
            win = "winner"

        self.id = (await config.GIVEAWAY_CHANNEL.send(":FaT: **GIVEAWAY** :FaT:",
              embed=discord.Embed(
                  color=discord.Color.green(),
                  title=self.prize,
                  timestamp=self.duration,
                  description=f"{self.description}Click the reaction below to enter!"
              ).set_footer(text=f"{str(self.winners)} {win} | Ends:").add_field(
                  name="Host:", value=(self.get_host()).mention, inline=False))).id

        await (await self.get_message()).add_reaction(config.GIVEAWAY_EMOJI.decode())

    async def end_giv(self):
        msg = await self.get_message()

        winners = await self.draw_winners(msg)

        if type(winners[0]) == discord.Member:
            text_1 = ""
            text_2 = ""
            for w in winners:
                text_1 += f"\n{w.mention}"
                text_2 += f"{w.mention}, "

            win_text = "Winners"
            if self.winners == 1:
                win_text = "Winner"
                text_1 = winners[0].mention

            await config.GIVEAWAY_CHANNEL.send(f"Congratulations {text_2[:-2]}! You won: {self.prize}!")
        else:
            win_text = "Winners"
            text_1 = winners[0]

        embed = msg.embeds[0]
        embed.color = discord.Color.dark_grey()
        embed.description = self.description
        embed.set_footer(text=f"{str(self.winners)} {win_text} | Ended:")
        embed.add_field(name=win_text+":", value=text_1, inline=False)

        await msg.edit(content=":FaT: **GIVEAWAY ENDED** :FaT:", embed=embed)

        db_remove_ids(self.id)

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

    def format_desc(self, description: tuple) -> str:
        desc = ""
        for s in description:
            desc += " " + s + " "

        return "\n" + desc + "\n"

    def get_host(self) -> discord.Member:
        return config.GUILD.get_member(self.host)

    async def get_message(self) -> discord.Message:
        return await config.GIVEAWAY_CHANNEL.fetch_message(self.id)

    async def draw_winners(self, msg: discord.Message) -> list:
        entered = []
        async for u in msg.reactions[0].users():
            if not u.bot:
                entered.append(u)

        if len(entered) < 1:
            await config.GIVEAWAY_CHANNEL.send(f"> The giveaway concluded with no winners.")
            return ["No one"]

        winners = []
        for _ in range(self.winners):
            try:
                w = entered[randrange(len(entered))]
            except ValueError:
                break
            winners.append(w)
            entered.remove(w)

        return winners

    # Errors
    class GiveawayWinnersError(commands.CommandError):
        pass

async def giv_end(giv_id):
    await (db_read_ids())[giv_id].end_giv()
