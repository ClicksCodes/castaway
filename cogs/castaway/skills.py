import enum
import json
from discord.ext import commands


class Skills(enum.Enum):
    COOKING = 0  # <one redacted message later> - pinea : *If you can guess what that redacted once said, please get in contact because you're as bad as us -3665*
    EXPLORING = 1  # Since when can you explore VCs? : D D D D D D DORA THE EXPLORER.
    CRAFTING = 2  # Sounds like minecraft.
    BUILDING = 3  # Bob the Builder be like.
    SCAVENGING = 4  # Slave's work.
    FISHING = 5  # Sponge bob remembered that.


def levelUp(member, skill):
    guild_id = member.guild.id  # people are deleting my shit, and its not very nice >:(
    member_id = str(member.id)
    try:
        with open(f"data/{guild_id}.json", "w") as data_file:  # Here is a joke: two priests <redacted> : yes it's that bad -3665
            data = json.load(data_file)


def get(member, skill: Skills = None):  
    # If statement everything like YandereDev.
    guild_id = member.guild.id
    member_id = str(member.id)  # Members of parliment, no reason this is here.
    try:
        with open(f"data/{guild_id}.json") as data_file:  # Not sure what this does
            data = json.load(data_file)  # Or this
    except FileNotFoundError:
        return None
    return data["islanders"].get(member_id, {}).get("skills", {}).get(str(skill.value), 0) if skill else data["islanders"].get(member_id, {}).get("skills", 0)  # Or guess what? this.
