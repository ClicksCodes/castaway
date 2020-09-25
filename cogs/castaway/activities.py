import enum  # FREKKING ENUM.
import json  # Day 01: words are starting to get <Redacted>, i cannot make any jokes on Catholic priest anymore.
from discord.ext import (
    commands,
)  # Commands are good too, you can use commands with this.
from . import errors  # Errors are good.
from . import islanders
from . import world
import datetime
import random


class Activities(enum.Enum):
    # Fact: Neither Minion or I (froggie) has a girlfriend, quite sad, i know -Frog. Nor does pinea but that's for other reasons. -TCP : kinda gay ngl -pinea
    """All the activies that players can do"""  # Activities. yes.
    COLLECTING = 0  # Collectin' stuff.
    FARMING = 1  # Farmin' stuff.
    # FARM_WATCHING = 2  # Fact: This code is 20% code and 80% comments. I'm Lovin' it.
    # FETCHING_WATER = 3  # Fetch some watur.


def _repeating_sample(population, k):
    assert len(sample) > 0  # There has to be something in the sample
    assert k >= 0  # We can't have negative sizes of k
    sample = []
    for i in range(k):
        sample.append(random.choice(population))
    return sample


activity_returns = (
    ((world.Wood, world.PlantFiber, world.Leaves), 1024),
    ((world.Wood, world.PlantFiber, world.Leaves), 256),
    None,
    None,
)


def calculate_returns_for(member, activity):
    activity = Activities(activity)
    minutes = 100
    return _repeating_sample(
        ((item, 1) for item in activity_returns[activity][0]),
        round((minutes * 256) / (minutes + activity_returns[activity][1])),
    )


def get_activity(member):
    return islanders.get_data_for(member)["activity"]


def stop_activity(member):
    data = islanders.get_data_for(member)
    activity = data["activity"]
    if activity is None:
        return
    returns = calculate_returns_for(member, activity)
    for item in returns:
        data["inventory"] = islanders.inventory_add(data["inventory"], *item)
    data["activity"] = None
    islanders.write_data_for(member, data)


def start_activity(member, activity):
    data = islanders.get_data_for(member)
    data["activity"] == {
        "start_time": datetime.datetime.now().timestamp(),
        "activity": activity.value,
    }
    islanders.write_data_for(member, data)


# how await message? nani? __init__.py line 98
def activity(
    activity_type: Activities,
):  # Activites again. : Good taste in music @3665 -TCP : Thanks -3665 : You're not welcome -TCP : Well ok then -3665
    """A decorator that marks a command as starting an activity"""  # We love decorators. : @mini maybe take in a number to determine how long it should take? -TCP : not quite how activites will work coded -3665 : ok -TCP

    def predicate(
        ctx,
    ):  # Nvidia Ctx, the 50th series, Ctx 5040 Ti will be sold at the cost of a liver. : sounds accurate -TCP : why... why do we... know this fact? how many livers have we bought that we just know what the price should be? -3665
        commands.guild_only().predicate(ctx)
        try:
            requires_game().predicate(ctx)
        except errors.NoGame:
            return False

        if get_activity(ctx.member) is not None:
            stop_activity(ctx.member)

        start_activity(ctx.member, activity_type)

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
