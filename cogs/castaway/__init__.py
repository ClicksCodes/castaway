from discord.ext import (
    commands,
)  # Who doesnt like importing stuff? I mean i sure like importing "Random" into my script. Im pretty sure we ARE going to need "Random" : Yes, we're going to need random. Good job commenter boy -3665
from . import creation
import discord


class Castaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["start, begin", "s"]
    )  # Second best thing in the code, the first one is darkmode. This starts the game. I know right?
    async def play(self, ctx):
        """This command will start the game will start."""

    @commands.command(aliases=["c", "col"])
    async def collect(self, ctx):
        """This command will make you start collecting some items- you'll need them."""  # Minecraft.

    @commands.command(aliases=["ex", "expl"])
    async def explore(self, ctx):
        """This command will make your character look around maybe finding new key place on the map."""  # No shit shelock, I dont think im gonna play with my eyes closed.

    @commands.command(aliases=["cr"])
    async def craft(self, ctx):
        """This command will let to craft some items to help throughout his journey. \nIt's not an old man from a cave that is going to give you a sword!"""  # Minecraft -- for some reason, minecraft always come back...

    @commands.command(aliases=["bl", "b"])
    async def build(self, ctx):
        """This command will let you build some structures around the predifined map."""

    @commands.group(aliases=["farms"], invoke_without_command=True)  # Farmin Simulatur
    async def farm(self, ctx):
        """This command will let you manage your farms."""

    @farm.command(
        name="plant", aliases=["pl"]
    )  # You know, you gotta make some money planting some weed. My bad, it's quite useful to survive, eating and such.
    async def farm_plant(self, ctx, farmid: int = 0):
        """This command will plant some culture in your farm(s), only works if you have a farm built!"""

    @farm.command(
        name="collect", aliases=["col", "c"]
    )  # How may war did the french win? Zero, they always surrendered.
    async def farm_collect(self, ctx, farmid: int = 0):
        """This command will make you able to collect all crops in a farm."""  # Slaves love this -- Slave remembered that.
        pass

    #  Might remove that one (?)
    @farm.command(name="watch")
    async def farm_collect(self, ctx):
        """This command will notify you if a farm is fully grown"""

    @commands.group(aliases=["mine"])
    async def mines(self, ctx):
        """This command will let you manage your mining."""

    @mines.command(name="mine", aliases=["m", "mi"])
    async def mines_mine(self, ctx, mineid: int = None):
        """This command will make you mine some ores, requires a tool."""

    @mines.command(name="transport", aliases=["tr", "t"])
    async def mines_transport(self, ctx, mineid: int = None):
        """This command will make you able to transport resources from mine to an area on a map, which can be sped up with a minecart."""

    """inventory commands"""

    @commands.group(aliases=["inv"], invoke_without_command=True)
    async def inventory(self, ctx):
        """This command will open your inventory."""
        await creation.Inventory.send(ctx=ctx)

    @inventory.command(name="craft")
    async def craft(self, ctx):
        data = creation.sendEmbed(ctx=ctx, cr_type="inv")
        await ctx.send(data[0])

        def check(msg):
            return (msg.content in data[1]) and (ctx.author == msg.author)

        msg = await self.bot.wait_for("message", check=check)
        newe = discord.Embed(
            title="Item Crafted",
            description=f"You have successfully crafted {msg.content}",
        )
        await ctx.send(embed=newe)

    # @commands.command(name="info")
    # async def info(self, ctx):
    #     embed = discord.Embed(
    #         title=f"{ctx.author.name}'s stats: Level {}"
    #     )

    #     await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Castaway(bot))
