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
    assert len(population) > 0  # There has to be something in the sample
    assert k >= 0  # We can't have negative sizes of k
    sample = []
    for _ in range(k):
        sample.append(random.choice(population))
    return sample


activity_returns = (
    ((world.Wood, world.PlantFiber, world.Leaves), 1024),
    ((world.Wood, world.PlantFiber, world.Leaves), 256),
    None,
    None,
)


def calculate_returns_for(member, activity):
    time = activity['start_time']
    activity = activity['activity']
    minutes = (datetime.datetime.now() - datetime.datetime.fromtimestamp(time)).seconds // 60
    return _repeating_sample(
        list(((item, 1) for item in activity_returns[activity][0])),
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
    data["activity"] = {
        "start_time": datetime.datetime.now().timestamp(),
        "activity": activity.value,
    }
    islanders.write_data_for(member, data)


# how await message? nani? __init__.py line 98
def activity(
    activity_type: Activities,
):  # Activites again. : Good taste in music @3665 -TCP : Thanks -3665 : You're not welcome -TCP : Well ok then -3665
    """A decorator that marks a command as starting an activity"""  # We love decorators. : @mini maybe take in a number to determine how long it should take? -TCP : not quite how activites will work coded -3665 : ok -TCP
    def inner(func):
        async def predicate(
            _cog,
            ctx,
        ):  # Nvidia Ctx, the 50th series, Ctx 5040 Ti will be sold at the cost of a liver. : sounds accurate -TCP : why... why do we... know this fact? how many livers have we bought that we just know what the price should be? -3665

            if get_activity(ctx.author) is not None:
                stop_activity(ctx.author)

            start_activity(ctx.author, activity_type)

            return True  # Truth. : Lies -TCP
        return commands.before_invoke(predicate)(requires_game()(func))  # Predictable. : Assignable predictiality -TCP
    return inner


def requires_game():
    """A decorator that requires a game to be active to pass"""

    async def predicate(ctx):
        await commands.guild_only().predicate(ctx)
        try:
            with open(f"data/{ctx.guild.id}.json") as data_file:
                data = json.load(data_file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise errors.NoData("There is not a game in {ctx.guild.id}")
        if not data["active"]:
            raise errors.NoGame("There is not a game in {ctx.guild.id}")
        return True

    return commands.check(predicate)

def requires_no_game():
    """A decorator that requires no active game to pass"""

    async def predicate(ctx):
        try:
            await requires_game().predicate(ctx)
            return False
        except (errors.NoGame, errors.NoData):
            return True

    return commands.check(predicate)