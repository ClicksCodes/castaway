import discord
from discord.ext import commands
import config
import traceback
from jishaku import help_command

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(*config.prefixes),
    allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False),
    status=discord.Status.dnd,
    activity=discord.Activity(
        type=discord.ActivityType.watching, name="discord go by."
    ),
    help_command=help_command.DefaultEmbedPaginatorHelp(),
)  # You know, the prefix, the thing you put before the command, like "!"

cogs = [
    "jishaku",  # Testing & debugging. it does seem useful, but I dont have a clue what the fuck this does -Froggie
    "cogs.castaway",  # The castaway game- y'know, the hekking game, the one that I'm procrastinating from making by writing this stupidly long and unnessecary comment please don't send me back there oh no it's coming goodbyeeee.eeeeeeeeee (don't forget me..........)
    "cogs.error_handler",
]


@bot.event
async def on_ready():
    print(
        f"Connected to discord as {bot.user}, ready to go!\n"
        f"You can invite me to your server at https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=60488"
    )  # A lot of people thought that Zelda was the main character in "the ledgend of zelda" it's actually Link.
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f"@{bot.user.name} help and being the god of Castaway Island",
        ),
    )


loaded = 0
total = len(cogs)
for cog in cogs:  # Coggin' it
    try:
        bot.load_extension(
            cog
        )  # anyone reading this is gonna have a great time, please vote for our game, not for the game but for the comments.
        loaded += 1
        print(f"Loaded cog {cog}, {loaded}/{total}")
    except Exception as e:  # Pet russian, I have gift for you: https://www.youtube.com/watch?v=p5L9-k0uV2A
        print(f"Failed to load cog {cog} : {e}")
        traceback.print_exc()

bot.run(
    config.token
)  # Anyone reading this, this project might become a time capsule, cause you know, all the shit inside will tell a lot later on in history, ou thoughts, ethics, ect... : not on the arctic code vault though :shrug: -3665
