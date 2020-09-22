from discord.ext import (
    commands,
)  # Who doesnt like importing stuff? I mean i sure like importing "Random" into my script. Im pretty sure we ARE going to need "Random" : Yes, we're going to need random. Good job commenter boy -3665
from . import UIs


class Castaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["start, begin"]
    )  # Second best thing in the code, the first one is darkmode. This starts the game. I know right?
    async def play(self, ctx):
        """Start the game"""

    @commands.command()
    async def collect(self, ctx):
        """Collect some items- you'll need them"""  # Minecraft.

    @commands.command()
    async def explore(self, ctx):
        """Take a look around"""  # No shit shelock, I dont think im gonna play with my eyes closed.

    @commands.command()
    async def craft(self, ctx):
        """Craft some items"""  # Minecraft -- for some reason, minecraft always come back...

    @commands.command()
    async def build(self, ctx):
        """Build structures"""

    @commands.group(aliases=["farms"], invoke_without_command=True)  # Farmin Simulatur
    async def farm(self, ctx):
        """Manage your farms"""

    @farm.command(
        name="plant"
    )  # You know, you gotta make some money planting some weed. My bad, it's quite useful to survive, eating and such.
    async def farm_plant(self, ctx, farmid: int = 0):
        """Plant some crops in your farm"""

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

    @inventory.command(name="craft")
    async def craft(self, ctx):
        UIs.Inventory.craft(self, ctx=ctx)


def setup(bot):
    bot.add_cog(Castaway(bot))
