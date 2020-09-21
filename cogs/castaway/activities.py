import enum  # FREKKING ENUM.
import json  # Day 01: words are starting to get <Redacted>, i cannot make any jokes on Catholic priest anymore.
from discord.ext import commands  # Commands are good too, you can use commands with this.
from . import errors  # Errors are good.


class Activities(enum.Enum):
    # Fact: Neither Minion or I (froggie) has a girlfriend, quite sad, i know -Frog. Nor does pinea but that's for other reasons. -TCP : kinda gay ngl -pinea
    """All the activies that players can do"""  # Activities. yes.
    COLLECT = 0  # Collectin' stuff.
    FARM_COLLECT = 1  # Farmin' stuff.
    FARM_OBSERVE = 2  # Fact: This code is 20% code and 80% comments. I'm Lovin' it.
    FETCH_WATER = 3  # Fetch some watur.

def activity(activity_type: Activities):  # Activites again. : Good taste in music @3665 -TCP : Thanks -3665 : You're not welcome -TCP : Well ok then -3665
    """A decorator that marks a command as starting an activity"""  # We love decorators. : @mini maybe take in a number to determine how long it should take? -TCP : not quite how activites will work coded -3665 : ok -TCP
    def predicate(ctx):  # Nvidia Ctx, the 50th series, Ctx 5040 Ti will be sold at the cost of a liver. : sounds accurate -TCP : why... why do we... know this fact? how many livers have we bought that we just know what the price should be? -3665
        try:
            requires_game().predicate(ctx):
        except errors.NoGame:
            return False
        return True  # Truth. : Lies -TCP

    return commands.check(predicate)  # Predictable. : Assignable predictiality -TCP

def requires_game():
    """A decorator that requires a game to be active to pass"""
    def predicate(ctx):
        try:
            with open(f"data/{ctx.guild.id}.json") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            raise errors.NoData("There is not a game in {ctx.guild.id}")
        if not data["active"]:
            raise errors.NoGame("There is not a game in {ctx.guild.id}")
        return True

    return commands.check(predicate)
