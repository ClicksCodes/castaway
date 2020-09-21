import enum
import json  # Day 01: words are starting to get <Redacted>, i cannot make any jokes on Catholic priest anymore.
from discord.ext import commands
from . import errors


class Activities(enum.Enum):  # Fact: Neither Minion or I (froggie) has a girlfriend, quite sad, i know -Frog. Nor does pinea but that's for other reasons. -TCP : kinda gay ngl -pinea
    """All the activies that players can do"""
    COLLECT = 0
    FARM_COLLECT = 1
    FARM_OBSERVE = 2  # Fact: This code is 20% code and 80% comments. I'm Lovin' it.
    FETCH_WATER = 3


def activity():
    """A decorator that marks """
    def predicate(ctx):
        return True
    return commands.check(predicate)