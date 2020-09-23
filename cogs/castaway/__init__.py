from discord.ext import (
    commands,
)  # Who doesnt like importing stuff? I mean i sure like importing "Random" into my script. Im pretty sure we ARE going to need "Random" : Yes, we're going to need random. Good job commenter boy -3665
from . import UIs


class Castaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["start, begin", "s"]
    )  # Second best thing in the code, the first one is darkmode. This starts the game. I know right?
    async def play(self, ctx):
        """When this command is sent, the game will start. \nAliases: play, start, begin, s"""

    @commands.command(aliases=["c", "col"])
    async def collect(self, ctx):
        """When this command is sent and a game is currently happening, you will start collecting some items- you'll need them. \nAliases: collect, c, col"""  # Minecraft.

    @commands.command(aliases=["ex", "expl"])
    async def explore(self, ctx):
        """When this command is sent and a game is currently happening, your character will start looking around maybe finding new key place on the map. \nAliases: explore, ex, expl"""  # No shit shelock, I dont think im gonna play with my eyes closed.

    @commands.command(aliases=["cr"])
    async def craft(self, ctx):
        """When this command is sent and a game is currently happening, your character will have the choice to craft some items to help throughout his journey. \nIt's not an old man from a cave that is going to give you a sword! \nAliases: craft, cr"""  # Minecraft -- for some reason, minecraft always come back...

    @commands.command(aliases=["bl", "b"])
    async def build(self, ctx):
        """When this command is sent and a game is currently happening, your character will have the choice to build some structures around the predifined map. \nAliases: build, bl, b"""

    @commands.group(
        aliases=["farms", "fa"], invoke_without_command=True
    )  # Farmin Simulatur
    async def farm(self, ctx):
        """When this command is sent and a game is currently happening, you will be able to manage your farms if you have any- they can be built from the build command. \nAliases: farm, farms, fa"""

    @farm.command(
        name="plant", aliases=["pl"]
    )  # You know, you gotta make some money planting some weed. My bad, it's quite useful to survive, eating and such.
    async def farm_plant(self, ctx, farmid: int = 0):
        """When this command is sent and a game is currently happening, you will be able to plant some plant in your farm, only works if you have a farm built! \nAliases: plant, pl"""

    @farm.command(name="collect")
    async def farm_collect(self, ctx, farmid: int = 0):
        """Collect all crops in a farm"""  # Slaves love this -- Slave remembered that.

    @farm.command(name="watch")
    async def farm_collect(self, ctx):
        """Get notified when a farm is fully grown"""  # How may war did the french win? Zero, they always surrendered.

    @commands.group()
    async def mines(self, ctx):
        """Manage mining"""

    @mines.command(name="mine")
    async def mines_mine(self, ctx, mineid: int = None):
        """Mine stuff"""

    @mines.command(name="transport")
    async def mines_transport(self, ctx, mineid: int = None):
        """transport resources from mine to an area on a map, can be sped up with a minecart"""

    """inventory commands"""

    @commands.group(aliases=["inv"], invoke_without_command=True)
    async def inventory(self, ctx):
        """manage inv"""
        await UIs.Inventory.send(ctx)

    @inventory.command(name="craft")
    async def craft(self, ctx):
        await UIs.Inventory.craft(ctx)


def setup(bot):
    bot.add_cog(Castaway(bot))
