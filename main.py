import discord
from discord.ext import commands
import json

with open("config.json") as config_file:
    config = json.load(config_file)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(["]"], ["¯\_(ツ)_/¯"])
)  # You know, the prefix, the thing you put before the command, like "!"

cogs = [
    "jishaku",  # Testing & debugging. it does seem useful, but I dont have a clue what the fuck this does -Froggie
    "cogs.castaway",  # The castaway game- y'know, the hekking game, the one that I'm procrastinating from making by writing this stupidly long and unnessecary comment please don't send me back there oh no it's coming goodbyeeee.eeeeeeeeee (don't forget me..........)
]


@bot.event
async def on_ready():
    print(
        "Connected to discord as {bot.user}, ready to go!"
    )  # A lot of people thought that Zelda was the main character in "the ledgend of zelda" it's actually Link.


loaded = 0
total = len(cogs)
for cog in cogs:  # Coggin' it
    try:
        bot.load_extension(
            cog
        )  # anyone reading this is gonna have a great time, please vote for our game, not for the game but for the comments.
        print(f"Loaded cog {cog}, {loaded}/{total}")
    except Exception as e:  # Pet russian, I have gift for you: https://www.youtube.com/watch?v=p5L9-k0uV2A
        print(f"Failed to load cog {cog} : {e}")

bot.run(
    config["token"]
)  # Anyone reading this, this project might become a time capsule, cause you know, all the shit inside will tell a lot later on in history, ou thoughts, ethics, ect...
