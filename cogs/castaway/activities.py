import enum
import json  # Day 01: words are starting to get <Redacted>, i cannot make any jokes on Catholic priest anymore.
from discord.ext import commands

class Activities(enum.Enum):  # Fact: Neither Minion or I (froggie) has a girlfriend, quite sad, i know -Frog. Nor does pinea but that's for other reasons. -TCP : kinda gay ngl -pinea
    """All the activies that players can do"""
    COLLECT = 0
    FARM_COLLECT = 1
    FARM_OBSERVE = 2  # Fact: This code is 20% code and 80% comments. I'm Lovin' it.
    FETCH_WATER = 3

def playing():
    def predicate(ctx):
        return game_in_progress(ctx.guild)  # Fact: ClicksMinutePer (also known as DragDev) is actually a <Redacted>, and we love it : no no dont tell them -pinea
    return commands.check(predicate)

def free():
    def predicate(ctx):
        return check_free(ctx.author)  # ClicksMinutePer isn't DragDev, it's the other way around. Get it right, slave -3665. Sowwy master -Frog : OwO harder master -pinea : <- to people who are reading the comments, note that this *wasn't* redacted and yet the other thing was. I'm just saying -3665
    return commands.check(predicate)

def game_in_progress(guild):
    guild_id = guild.id  # Froggie is actually in charge of all the comments, good to know right? 
    try:
        with open(f"data/{guild_id}.json") as data_file:  # This game is going to be either Communism or Capitalism, i bet on Communism cause you know, Communism.
            data = json.load(data_file)
    except FileNotFoundError:
        data = {"active": False}
    return data["active"];  # Who doesnt like a good semi-colon at the end of their line? oh, nevermind. Python am i right?

def check_free(member):
    guild_id = member.guild.id  # Minion never played The Ledgend Of Zelda by the way. What a shame. That why im a slave now, cause im better than him. That doesnt seem right...
    member_id = str(member.id)
    try:
        with open(f"data/{guild_id}.json") as data_file:  # Dam, look a those line of codes, some of them have bloody semi-colons, quite like them actually.
            data = json.load(data_file)
    except FileNotFoundError:
        data = {"active": False}  # Wow, look at all of those... Lovely Javascript code piece everywhere. It's not python, im telling you (it's actually python, dont get confused, this sentence is useless, like every other one).
    return not data["active"] \
        or bool(data["islanders"].get(member_id, {}).get("action", None))  # Tips: never look away from the code, it might happen that some of it appears like pokemons; randomly.

def set_activity(member, activity: Activities):
    guild_id = member.guild.id 
    member_id = str(member.id)
    try:
        with open(f"data/{guild_id}.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        data = {"active": False}
    if not data["active"]:
        return
    data["islanders"][member_id]


