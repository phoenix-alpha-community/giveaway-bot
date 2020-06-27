"""
This module is used to host the Giveaway class.
"""

import config
import discord
import decimal
import other
import pytimeparse
import re
from database import db_read_ids, db_remove_ids
from datetime import datetime, timedelta
from dateutil import parser
from discord.ext import commands
from random import randrange
from scheduling import deschedule


class Giveaway:
    """
    This class contains every information needed during the lifespan of a giveaway.

    Attributes:
        winners (int): The amount of winners of the giveaway.
        duration (str): The time before, or at which, the giveaway ends.
                        See the help message for time formats.
        prize (str): The prize of the giveaway.
        description (tuple): The description of the giveaway.
        host (discord.Member): The member who started the giveaway.

    Returns:
        None
    """

    def __init__(self, winners: int, duration: str, prize: str,
                 description: str, host: discord.Member):
        # Check if the number of winners is lower or equal to 0. If it is, raise an error.
        if winners <= 0:
            raise self.GiveawayLowWinnersError

        # Check if the number of winners is higher than the max amount of winners. If it is, raise an error.
        if winners > config.WINNERS_MAX_AMOUNT:
            raise self.GiveawayHighWinnersError

        self.duration = self.convert_dur(duration)  # The duration of the giveaway. (type: datetime.datetime)
        self.description = description  # The description of the giveaway. (type: str)
        self.host = host.id  # The id of the member who started the giveaway. (type: int)
        self.id = None  # *Check doc below*
        self.prize = prize  # The prize of the giveaway. (type: str)
        self.timer_id = None  # The id of the "timer". Assigned later.
        self.winners = winners  # The amount of members that can win. (type: int)

        """
        id (int): The id of the giveaway message. This is also used to
                  identify the giveaway. It's value is assigned later
                  during the giveaway creation (create_giv).
        """

    # Internal functions: primary purpose
    async def create_giv(self) -> None:
        """
        Creates a giveaway in the giveaway channel.

        Attributes:
            None

        Returns:
            None
        """

        win = "winners"
        if self.winners == 1:
            win = "winner"

        # Send the giveaway message. Save it's id.
        self.id = (await config.GIVEAWAY_CHANNEL.send(f"{config.GIVEAWAY_TITLE_EMOJI}"
                                      f" **GIVEAWAY** {config.GIVEAWAY_TITLE_EMOJI}",
              embed=discord.Embed(
                  color=discord.Color.green(),
                  title=self.prize,
                  timestamp=self.duration,
                  description=f"{self.description}Click the reaction below to enter!"
              ).set_footer(text=f"{str(self.winners)} {win} | Ends:").add_field(
                  name="Host:", value=(self.get_host()).mention, inline=False))).id

        # Add the first reaction to the giveaway message.
        await (await self.get_message()).add_reaction(config.GIVEAWAY_EMOJI.decode())

    async def end_giv(self):
        """
        Ends the giveaway.

        Attributes:
            None

        Returns:
            None
        """

        try:
            msg = await self.get_message()  # Get the message object of the giveaway. (type: discord.Message)
        except discord.errors.NotFound:
            print("====DISCLAMER:====\nIf the error below is \"other.InexistentMessageError\" it can be ignored.\n========")
            raise other.InexistentMessageError

        winners = await draw_winners(msg, self.winners)  # Draw the winners of the giveaway. (type: list)

        # Check if the first winner is a member object.
        if type(winners[0]) == discord.Member:
            # Format the text for the giveaway message
            text_1 = ""
            text_2 = ""
            for w in winners:
                text_1 += f"\n{w.mention}"
                text_2 += f"{w.mention}, "

            win_text = "Winners"
            if self.winners == 1:
                win_text = "Winner"
                text_1 = winners[0].mention

            # Format the embed for the giveaway message
            embed = discord.Embed(
                title="The Giveaway ended!",
                color=discord.Color.green(),
                description=f"Congratulations {text_2[:-2]}! You won: {self.prize}!\n"
                            f"__[Click here]({msg.jump_url})__ to go to the giveaway."
            )

            # Send the embed in the giveaway channel and react to it with the "clapping hands" emoji.
            await (await config.GIVEAWAY_CHANNEL.send(embed=embed))\
                .add_reaction(b"\xF0\x9F\x91\x8F".decode())

        else:  # This is likely because no one won the giveaway.
            win_text = "Winners"
            text_1 = winners[0]

        # Edit the giveaway message.
        embed = msg.embeds[0]
        embed.color = discord.Color.dark_grey()
        embed.description = self.description
        embed.set_footer(text=f"{str(self.winners)} {win_text} | Ended:")
        embed.add_field(name=win_text+":", value=text_1, inline=False)  # Add a field with as value, the winners of the giveaway.

        await msg.edit(content=":FaT: **GIVEAWAY ENDED** :FaT:", embed=embed)

        deschedule(self.timer_id)  # Remove the giveaway timer. This makes sure no errors occur in case the giveaway was closed manually.
        db_remove_ids(self.id)  # Remove the giveaway from the database.

    # Internal functions: secondary purpose
    def convert_dur(self, dur) -> datetime:
        """
        Converts the duration from str to datetime.datetime
        It uses multiple modules to cover different type of time-formats.

        Attributes:
            dur (str): The duration to be converted.

        Returns:
            datetime.datetime: The converted duration.
        """

        def _add():
            # Check if the duration begins with "+". If it doesn't, return False.
            if not dur.startswith("+"):
                return False

            dt = datetime.now(config.TIMEZONE)  # Get the current time.
            try:
                delta = timedelta(seconds=pytimeparse.parse(dur[1:].lower()))  # Get the timedelta of the giveaway.
            except TypeError:
                return False  # Return false if the date could not be parsed.

            return dt + delta  # Return the current time + the timedelta given.

        time = _add()

        # Check if the time is False. If it is parse the str with parser.parse()
        if not time:
            try:
                time = config.TIMEZONE.localize(parser.parse(dur.replace("+", "")))  # Get the datetime of the giveaway.
            except ValueError or decimal.InvalidOperation:
                raise self.GiveawayInvalidDuration  # Raise error if the given str could not be parsed.

        else:
            time = time.replace(second=0, microsecond=0)  # Round the time.

        # Check if the given datetime is in the past. If it is, raise an error.
        if time < datetime.now(config.TIMEZONE):
            raise self.GiveawayPastDateError

        # Check if the given datetime is more than 365 days away (1 year). If it is, raise an error.
        if datetime.now(config.TIMEZONE) + timedelta(days=365) < time:
            raise self.GiveawayFutureDateError

        return time  # Return the datetime

    def get_host(self) -> discord.Member:
        """
        Get the member object of the member who started the giveaway,
        using it's id.

        Attributes:
            None

        Returns:
            discord.Member: The member who started the giveaway.
        """

        return config.GUILD.get_member(self.host)

    async def get_message(self) -> discord.Message:
        """
        Get the message object of the giveaway message using it's id.

        Attributes:
            None

        Returns:
            discord.Message: The giveaway message.
        """

        return await config.GIVEAWAY_CHANNEL.fetch_message(self.id)

    # Errors
    class GiveawayLowWinnersError(commands.CommandError):
        """
        This error gets raised only in the giveaway __init__ function.
        It gets raised when the amount of winners is lower or equal to 0
        """
        pass

    class GiveawayHighWinnersError(commands.CommandError):
        """
        This error gets raised only in the giveaway __init__ function.
        It gets raised when the amount of winners is higher than config.WINNERS_MAX_AMOUNT
        """
        pass

    class GiveawayPastDateError(commands.CommandError):
        """
        This error gets raised only in the giveaway convert_dur function.
        It gets raised when the given date is in the past.
        """
        pass

    class GiveawayFutureDateError(commands.CommandError):
        """
        This error gets raised only in the giveaway convert_dur function.
        It gets raised when the given date is more than 365 days away (1 year).
        """
        pass

    class GiveawayInvalidDuration(commands.CommandError):
        """
        This error gets raised only in the giveaway convert_dur function.
        It gets raised when the given duration could not be parsed.
        """
        pass


async def draw_winners(msg: discord.Message, amount: int, reroll: bool = False) -> list:
    """
    Draws the winners of the giveaway.

    Attributes:
        msg (discord.Message): The message object of the giveaway message.
        amount (int): The amount of winners to be drawn.
        reroll (bool): If this function has been summoned by the reroll command, set to True.

    Returns:
        list: The list of member who where drawn.
    """

    # Insert every member who reacted to the giveaway message, in a list.
    entered = []
    async for u in msg.reactions[0].users():
        if not u.bot:  # Make sure the member is not a bot account.
            entered.append(u)

    # Check if the function was called by the reroll command. If so, remove from entered all members who already won.
    if reroll:
        pattern = r"<@([0-9]+)>"
        for match in re.finditer(pattern, msg.embeds[0].fields[1].value):
            entered.remove(config.GUILD.get_member(int(match.group(1))))

    # Check if the number of members who entered is bigger or equal to 1. If it's not return no winners.
    if len(entered) < 1:
        text = f"> **The giveaway concluded with no winners.**"
        if reroll:  # Check if the function was called by the reroll command. If so, change the text.
            text = f"> **No one else entered the giveaway**"
        await config.GIVEAWAY_CHANNEL.send(text)
        return ["No one"]

    winners = []
    for _ in range(amount):  # Repeat for the amount of members that can win.
        try:
            w = entered[randrange(len(entered))]  # Draw a winner from the list of members who entered.
        except ValueError:
            break  # Break the loop if there is no one left in the list
        winners.append(w)  # Append the drawn member to the list of winners.
        entered.remove(w)  # Remove the drawn member from the list of people who entered.

    return winners  # Return the list of winners

async def giv_end(giv_id):
    """
    Retrieves the giveaway object from the database and ends it.

    Attributes:
        giv_id (int): The id of the giveaway.

    Returns:
        None
    """

    try:
        await (db_read_ids())[giv_id].end_giv()
    except KeyError:
        return
