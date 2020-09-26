from discord.ext import (
    commands,
)  # Who doesnt like importing stuff? I mean i sure like importing "Random" into my script. Im pretty sure we ARE going to need "Random" : Yes, we're going to need random. Good job commenter boy -3665
from . import creation
from . import activities
from . import world
from . import islanders
import discord, math, time, humanize, datetime, json, io
from PIL import Image, ImageDraw
import numpy as np
import random


def farms_built():
    def predicate(ctx):
        with open(f"data/{ctx.guild.id}.json") as data_file:
            d = json.load(data_file)["structures"]
        if "farm" in d:
            return True
        else:
            raise errors.NoFarmsBuilt("No farms are built in the server")
    return commands.check(predicate)

class Castaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def generateMap(mapsize=(50,50), passes=10, seed=0):
        game = world.World(size=mapsize, passes=passes, seed=seed)

        return game, mapsize
    
    @staticmethod
    async def getMapImage(game, mapsize):
        mult = 1000 / (max((mapsize[0], mapsize[1])))

        dimensions = (mapsize[1] * int(mult), mapsize[0] * int(mult))

        def hex_to_rgb(value):
            lv = len(value)
            return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))

        colors = {
            "OCEAN": hex_to_rgb("71AFE5"),
            "JUNGLE": hex_to_rgb("60B358"),
            "CLIFF": hex_to_rgb("545454"),
            "LAKE": hex_to_rgb("78ECF2"),
            "SAND": hex_to_rgb("E6DC71"),
            "GRASS": hex_to_rgb("A1CC65"),
            "UNKNOWN": hex_to_rgb("000000"),
        }

        curMap = []

        for chunkRow in game.chunks:
            curRow = []
            for chunk in chunkRow:
                # if chunk.discovered == False and chunk.name == "OCEAN":
                #     curRow.append(colors[chunk.name])
                # else:
                #     curRow.append(colors["UNKNOWN"])
                curRow.append(colors[chunk.name])
            curMap.append(curRow)

        im = Image.fromarray(np.uint8(curMap), mode="RGB")
        im = im.resize(dimensions, 4)  # 0 4

        return im, curMap

    @commands.command(
        aliases=["start", "begin", "s"]
    )  # Second best thing in the code, the first one is darkmode. This starts the game. I know right?
    @commands.has_permissions(manage_guild=True)
    @activities.requires_no_game()
    async def play(self, ctx):
        """When this command is sent, the game will start."""
        mapsize = (50, 50)
        passes = 4
        seed = random.randint(0, 1000000000000000)

        returned, dim = await self.generateMap(mapsize=mapsize, passes=passes, seed=seed)
        world = returned
        image, mapArray = await self.getMapImage(world, dim)

        with open(f"data/{ctx.guild.id}.json", "w") as data_file:
            json.dump(
                {
                    "active": True,
                    "islanders": {},
                    "worldData": {
                        "mapsize": [50, 50],
                        "passes": 4,
                        "seed": world.seed
                    },
                    "structures": []
                },
                data_file
            )
        
        buf = io.BytesIO()
        image.save(buf, format="png")
        buf.seek(0)
        embed=discord.Embed(
            title="Game started!",
            description="I've started a game in your server. Good luck!",
        )
        embed.set_footer(text=f"Your game seed is {world.seed}")
        embed.set_image(url="attachment://map.png")
        return await ctx.send(
            embed=embed,
            file=discord.File(buf, filename="map.png")
        )
        buf.close()
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def quit(self, ctx):
        pass

    @commands.command(name="map")
    @activities.requires_game()
    async def map(self, ctx):
        with open(f"data/{ctx.guild.id}.json") as data_file:
            data = json.load(data_file)["worldData"]
        dimensions = (data["mapsize"][0], data["mapsize"][1])
        returned, dim = await self.generateMap(mapsize=dimensions, passes=data["passes"], seed=data["seed"])
        image, mapArray = await self.getMapImage(returned, dimensions)

        buf = io.BytesIO()
        image.save(buf, format="png")
        buf.seek(0)
        embed=discord.Embed(
            title="Game map"
        )

        embed.set_footer(text=f"Your game seed is {data['seed']}")
        embed.set_image(url="attachment://map.png")
        return await ctx.send(
            embed=embed,
            file=discord.File(buf, filename="map.png")
        )
        buf.close()

    @commands.command(aliases=["c", "col"])
    @activities.activity(activities.Activities.COLLECTING)
    async def collect(self, ctx):
        """Start collecting some items from around the world

You'll need them...
        """  # Minecraft.
        await ctx.send(embed=discord.Embed(
            title=f"You started collecting",
            description=f"Run `collect` again later to store items, as you'll get slower over time.",
            footer=f"{ctx.author}"
        ))

    @commands.command(aliases=["current", "currently"])
    async def activity(self, ctx):
        activity = islanders.get_data_for(ctx.author)["activity"]
        if activity is None:
            return await ctx.send(ctx.author.mention, embed=discord.Embed(
                title=f'You are currently being a developer on our team',
                description=f'And by that we mean doing nothing. Try running `@{ctx.bot.user.name} collect` to start getting some items'
            ), allowed_mentions=discord.AllowedMentions(users=[ctx.author]))
        activity_name = activities.Activities(activity["activity"]).name.lower()
        await ctx.send(embed=discord.Embed(
            title=f'You are currently {activity_name}',
            description=f'You started {humanize.naturaltime(datetime.datetime.now() - datetime.datetime.fromtimestamp(activity["start_time"]))}',
            footer=f"{ctx.author}"
        ))

    @commands.command(aliases=["ex", "expl"])
    async def explore(self, ctx):
        """This command will make you look around and finding place on the map."""  # No shit shelock, I dont think im gonna play with my eyes closed.

    @commands.command(aliases=["bl", "b"])
    @commands.max_concurrency(1, per=commands.BucketType.member, wait=False)
    async def build(self, ctx):
        """This command will let you build some structures around the map."""
        data = islanders.get_data_for(ctx.author)

        buildings = ""
        possible = []
        n = 1
        for item in creation.flatten(creation.Crafting.menu):
            if item in data["inventory"]["items"]:
                possible.append(item.name)
                buildings += f"\n[{n}] {item}"
                n += 1
        
        await ctx.send(embed=discord.Embed(
            title="Placeable buildings",
            description=buildings or "*You do not have any buildings in your inventory*"
        ))

        if n == 1: return

        msg = ctx.bot.wait_for("message", check = lambda msg : msg.author == ctx.author)
        try: ctnt = int(msg.message.content)
        except: return

        if 0 < ctnt < n:
            with open(f"data/{ctx.guild.id}.json") as data_file:
                d = json.load(data_file)
            d["structures"].append(possible[ctnt-1].value)
            with open(f"data/{ctx.guild.id}.json", "w") as data_file:
                json.dump(d, data_file)


    # @commands.group(aliases=["farms", "f"], invoke_without_command=True)  # Farmin Simulatur
    # async def farm(self, ctx):
    #     """This command will let you manage your farms."""

    # @farm.command(
    #     name="plant", aliases=["pl"]
    # )  # You know, you gotta make some money planting some weed. My bad, it's quite useful to survive, eating and such.
    # async def farm_plant(self, ctx, farmid: int = 0):
    #     """This command will plant some culture in your farm(s), only works if you have a farm built!"""

    @commands.command(
        name="farm", aliases=["f", "fa"]
    )  # How may war did the french win? Zero, they always surrendered. : to add context- the_froggie is french. I'm not 100% sure why he's saying this but I'm going to allow it -mini
    @farms_built()
    @activities.activity(activities.Activities.FARMING)
    async def farm_collect(self, ctx, farmid: int = 0):
        """Collect crops from a farm

Similar to collecting but faster
"""  # Slaves love this -- Slave remembered that.
        await ctx.send(embed=discord.Embed(
            title=f"You've started farming",
            description=f"Run `farm` again later to store your items, as you'll get slower over time.",
            footer=f"{ctx.author}"
        ))


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

    @inventory.group(name="craft", invoke_without_command=True)
    @commands.max_concurrency(1, per=commands.BucketType.member, wait=False)
    async def craft(self, ctx):
        data = creation.Inventory.sendCraftables(ctx=ctx, cr_type="inv")
        await ctx.send(embed=data[0])

        print(data[1])

        def check(msg):
            try:
                return (0 < int(msg.content) <= len(data[1])) and (ctx.author == msg.author)
            except: 
                return False

        msg = await self.bot.wait_for("message", check=check)

        player_data = islanders.get_data_for(ctx.author)
        for ingredient, amount in data[1][int(msg.content)-1].recipe.items():
            player_data["inventory"], success = islanders.inventory_remove(player_data["inventory"], ingredient, amount)
            if not success:
                raise OutOfItemsError(f"You don't have enough {ingredient} to craft this")

        player_data["inventory"], success = islanders.inventory_add(player_data["inventory"], data[1][int(msg.content)-1], 1)
        if not success:
            return await ctx.send("You don't have enough inventory space to fit the crafted item. Trash something first...")
        islanders.write_data_for(ctx.author, player_data)


        newe = discord.Embed(
            title="Item Crafted",
            description=f"You have successfully crafted {data[1][int(msg.content)-1].name}",
            footer=f"{ctx.author}"
        )
        await ctx.send(embed=newe)

    @craft.command(name="list")
    async def craft_list(self, ctx, craftable_type="all"):
        data = creation.Inventory.sendAllCraftables(ctx=ctx, cr_type=craftable_type)
        await ctx.send(embed=data[0])

    @commands.command(name="craft", aliases=["cr"])
    async def _craft(self, ctx):
        await self.craft.invoke(ctx)

    # @commands.command(name="info")
    # async def info(self, ctx):
    #     embed = discord.Embed(
    #         title=f"{ctx.author.name}'s stats: Level {}"
    #     )

    #     await ctx.send(embed=embed)

    @commands.group(name="storage", invoke_without_command=True)
    async def storage(self, ctx):
        pass

    #@store.command()
    #async def store(self, ctx):
    #    pass


def setup(bot):
    bot.add_cog(Castaway(bot))
