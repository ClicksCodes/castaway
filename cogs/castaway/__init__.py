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
from jishaku import paginators
import typing
import os

dedicated_servers = []


class FakeItemTM:
    def __init__(self, name):
        self.name = name


def dedicated_only():
    def predicate(ctx):
        if ctx.guild.id in dedicated_servers:
            return True
        else:
            return False


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
    async def generateMap(mapsize=(50, 50), passes=10, seed=0):
        game = world.World(size=mapsize, passes=passes, seed=seed)

        return game, mapsize

    @staticmethod
    @dedicated_only()
    async def assignChannels(ctx, world):
        channels_by_coord = []

        no_one = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }

        category = await ctx.guild.create_category(
            "Castaway", reason="Game Started. Play on!"
        )

        for row in world:
            tmp_channels = []
            for chunk in row:
                new_channel = await category.create_text_channel(
                    f"{chunk.name}",
                    overwrites=no_one,
                    topic=f"X:{chunk.coorinates[0]} / Y:{chunk.coorinates[1]} || Buildings: None",
                    reason="Generating...",
                )
                tmp_channels.append(new_channel.id)
            channels_by_coord.append(tmp_channels)

        with open(f"data/{ctx.guild.id}.json") as data_file:
            old = json.load(data_file)
            old["category"] = category.id
            old["channels"] = channels_by_coord
        with open(f"data/{ctx.guild.id}.json", "w") as data_file:
            json.dump(old, data_file)

        return (category.id, channels_by_coord)

    async def show_channel(self, member, coords: tuple = None):
        with open(f"data/{member.guild.id}.json") as data_file:
            guild_file = json.load(data_file)
            channels = guild_file.get("channels", None)
        channel_id = channels[coords[1]][coords[0]]
        channel = self.bot.get_channel(channel_id)

        perms = channel.overwrites_for(member)
        perms.read_messages = True
        perms.send_messages = True
        await channel.set_permissions(member, overwrites=perms)

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

    @commands.command()
    @activities.requires_game()
    async def buildings(self, ctx):
        build_types = {}
        with open(f"data/{ctx.guild.id}.json") as data_file:
            builds = json.load(data_file)["structures"]
        for item in builds:
            build_types[item] = build_types.get(item, 0) + 1
        await ctx.send(
            "**You have built**:\n"
            + (
                "\n".join(f"{build}: {amount}" for build, amount in build_types.items())
                or "*Nothing. Like the amount of sleep I got tonight (last night of pyweek).*"
            )
        )

    @commands.command()
    async def tutorial(self, ctx):
        pages = paginators.PaginatorEmbedInterface(
            ctx.bot, commands.Paginator(prefix="", suffix="", max_size=1991)
        )
        await pages.add_line(
            "**TUTORIAL**\nWelcome to Castaway! Your goal is to escape the island by collecting resources and crafting items to escape. Here, you can find the essential commands for island survival."
        )
        await pages.add_line(
            f"**BASIC COMMANDS**\nHere is the list of simple and useful commands you will need\n"
            f"`@{ctx.bot.user.name}inventory` - Shows the items in your inventory\n"
            f"`@{ctx.bot.user.name}map` - Shows a map of your island\n"
            f"`@{ctx.bot.user.name}store` - Shows the items in the shared storage\n"
            f"`@{ctx.bot.user.name}store add {{amount}} {{item}}` - Adds an item to the storage\n"
            f"`@{ctx.bot.user.name}store take {{amount}} {{item}}` - Takes some items from storage\n"
        )
        await pages.add_line(
            f"**CRAFTING**\nTo unlock new items you'll need to craft. *Please note, some items need buildings to be placed in order to craft*\n"
            f"`@{ctx.bot.user.name}craft` - Craft up some items\n"
            f"`@{ctx.bot.user.name}craft list` - Show a list of all possible items that you can craft (warning: it's long)\n"
        )
        await pages.add_line(
            f"**COLLECTING**\nTo get enough resources to craft, you'll need to collect items. **These commands are meant to be run while idling. You will not instantly get items, please wait a few minutes before trying to put the items you've collected into your inventory**\n"
            f"`@{ctx.bot.user.name}collect` - Collect some items that you find lying around your island. You must run `collect` again to put the items into your inventory\n"
            f"`@{ctx.bot.user.name}mine` - Mine some ores from some caves on the island. You must run `mine` again to put the items into your inventory\n"
        )
        await pages.add_line(
            f"**FARMING**\nFarming is a much quicker way to get plant-based items such as fiber and leaves\n"
            f"`@{ctx.bot.user.name}farm` - Begin farming. You must have a farm to do so\n"
            f"`@{ctx.bot.user.name}build` - Build a building, such as a farm or a workbench. You must have one in your inventory. Please refer to the crafting section to obtain these\n"
        )
        await pages.add_line(
            f"**BUILDING**\nSome tasks, such as crafting special items or farming need buildings. You can craft buildings before placing them\n"
            f"`@{ctx.bot.user.name}craft` - Craft the buildings before placing them\n"
            f"`@{ctx.bot.user.name}build` - Build a building, such as a farm or a workbench. You must have one in your inventory. Please refer to the crafting section to obtain these\n"
        )
        await pages.add_line(
            f"**OTHER**\nThere's a few things we haven't mentioned\n"
            f"`@{ctx.bot.user.name}play` - Start a game. You will need manage server to do this\n"
            f"`@{ctx.bot.user.name}quit` - Quit a game without finishing. You will need administrator to do this\n"
            f"`@{ctx.bot.user.name}win` - Use resources in server storage to build a boat and win\n"
            f"In addition, please note that player inventories are limited to 8 slots of 32 items each. You won't be able to get any more when your inventory is full"
        )
        await pages.send_to(ctx)

    @commands.command(
        aliases=["start", "begin"]
    )  # Second best thing in the code, the first one is darkmode. This starts the game. I know right?
    @commands.has_permissions(manage_guild=True)
    @activities.requires_no_game()
    async def play(self, ctx):
        """When this command is sent, the game will start."""
        mapsize = (50, 50)
        passes = 4
        seed = random.randint(0, 1000000000000000)

        returned, dim = await self.generateMap(
            mapsize=mapsize, passes=passes, seed=seed
        )
        world = returned
        image, mapArray = await self.getMapImage(world, dim)

        with open(f"data/{ctx.guild.id}.json", "w") as data_file:
            json.dump(
                {
                    "active": True,
                    "start_time": datetime.datetime.now().timestamp(),
                    "islanders": {},
                    "worldData": {"mapsize": [50, 50], "passes": 4, "seed": world.seed},
                    "structures": [],
                },
                data_file,
            )

        buf = io.BytesIO()
        image.save(buf, format="png")
        buf.seek(0)
        embed = discord.Embed(
            title="Game started!",
            description="I've started a game in your server. Good luck!",
        )
        embed.set_footer(text=f"Your game seed is {world.seed}")
        embed.set_image(url="attachment://map.png")
        return await ctx.send(embed=embed, file=discord.File(buf, filename="map.png"))
        buf.close()

    @commands.command(aliases=["kill", "exit"])
    @commands.has_permissions(administrator=True)
    @activities.requires_game()
    async def quit(self, ctx):
        await ctx.send(
            f"{ctx.author.mention}, if you are **certain** you want to leave the island and end the game please type `yes I am sure` as your next message"
        )
        response = (
            await ctx.bot.wait_for(
                "message",
                check=lambda message: message.channel == ctx.channel
                and message.author == ctx.author,
            )
        ).content
        if response.lower() == "yes i am sure":
            os.remove(f"data/{ctx.guild.id}.json")
            return await ctx.send(f"Goodbye world :wave:")
        else:
            await ctx.send("Cancelled deleting the game")

    @commands.command(name="map")
    @activities.requires_game()
    async def map(self, ctx):
        with open(f"data/{ctx.guild.id}.json") as data_file:
            data = json.load(data_file)["worldData"]
        dimensions = (data["mapsize"][0], data["mapsize"][1])
        returned, dim = await self.generateMap(
            mapsize=dimensions, passes=data["passes"], seed=data["seed"]
        )
        image, mapArray = await self.getMapImage(returned, dimensions)

        buf = io.BytesIO()
        image.save(buf, format="png")
        buf.seek(0)
        embed = discord.Embed(title="Game map")

        embed.set_footer(text=f"Your game seed is {data['seed']}")
        embed.set_image(url="attachment://map.png")
        return await ctx.send(embed=embed, file=discord.File(buf, filename="map.png"))
        buf.close()

    @commands.command(aliases=["c", "col"])
    @activities.activity(activities.Activities.COLLECTING)
    async def collect(self, ctx):
        """Start collecting some items from around the world

        You'll need them...
        """  # Minecraft.
        await ctx.send(
            embed=discord.Embed(
                title=f"You started collecting",
                description=f"Run `collect` again later to store items, as you'll get slower over time.",
                footer=f"{ctx.author}",
            )
        )

    @commands.command(aliases=["current", "currently"])
    @activities.requires_game()
    async def activity(self, ctx):
        activity = islanders.get_data_for(ctx.author)["activity"]
        if activity is None:
            return await ctx.send(
                ctx.author.mention,
                embed=discord.Embed(
                    title=f"You are currently being a developer on our team",
                    description=f"And by that we mean doing nothing. Try running `@{ctx.bot.user.name} collect` to start getting some items",
                ),
                allowed_mentions=discord.AllowedMentions(users=[ctx.author]),
            )
        activity_name = activities.Activities(activity["activity"]).name.lower()
        await ctx.send(
            embed=discord.Embed(
                title=f"You are currently {activity_name}",
                description=f'You started {humanize.naturaltime(datetime.datetime.now() - datetime.datetime.fromtimestamp(activity["start_time"]))}',
                footer=f"{ctx.author}",
            )
        )

    #    @commands.command(aliases=["ex", "expl"])
    #    async def explore(self, ctx):
    #        """This command will make you look around and finding place on the map."""  # No shit shelock, I dont think im gonna play with my eyes closed.

    @commands.command(aliases=["bl", "b"])
    @activities.requires_game()
    @commands.max_concurrency(1, per=commands.BucketType.member, wait=False)
    async def build(self, ctx):
        """This command will let you build some structures around the map."""
        data = islanders.get_data_for(ctx.author)

        buildings = ""
        possible = []
        n = 0

        for item in creation.flatten(creation.Crafting.menu):
            if item.name in [item[0] for item in data["inventory"]["items"]]:
                possible.append(item)
                n += 1
                buildings += f"\n[{n}] {item.name}"

        def check(msg):
            try:
                return (ctx.author == msg.author) and (0 < int(msg.content) <= n)
            except:
                return False

        await ctx.send(
            embed=discord.Embed(
                title="Placeable buildings",
                description=buildings
                or "*You do not have any buildings in your inventory*",
            )
        )

        if n == 0:
            return

        msg = await ctx.bot.wait_for("message", check=check)
        ctnt = int(msg.content)  # content - pinea

        if 0 < ctnt <= n:
            data["inventory"], success = islanders.inventory_remove(
                data["inventory"], possible[ctnt - 1], 1
            )  # content - pinea
            if not success:
                raise OutOfItemsError(
                    f"You don't have enough {possible[ctnt-1].name} to build this"
                )  # ctnt, you mean <redacted>? -3665 : no, it stands for content -pinea
            with open(f"data/{ctx.guild.id}.json") as data_file:
                d = json.load(data_file)
            d["structures"].append(possible[ctnt - 1].name)  # content - pinea
            with open(f"data/{ctx.guild.id}.json", "w") as data_file:
                json.dump(d, data_file)
            islanders.write_data_for(ctx.author, data)
            await ctx.send(f"You built a {possible[ctnt-1].name}")  # content - pinea

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

        Similar to collecting but faster"""  # Slaves love this -- Slave remembered that.
        await ctx.send(
            embed=discord.Embed(
                title=f"You've started farming",
                description=f"Run `farm` again later to store your items, as you'll get slower over time.",
                footer=f"{ctx.author}",
            )
        )

    @commands.command(aliases=["m", "mi"])
    @activities.activity(activities.Activities.MINING)
    async def mine(self, ctx):
        """Start mining some ores

        No diamond ore in sight though- perhaps it's because we're not at y=12...
        """  # Minecraft.
        await ctx.send(
            embed=discord.Embed(
                title=f"You started collecting",
                description=f"Run `mine` again later to store items, as you'll get slower over time.",
                footer=f"{ctx.author}",
            )
        )

    """inventory commands"""

    @commands.group(aliases=["inv"], invoke_without_command=True)
    @activities.requires_game()
    async def inventory(self, ctx):
        """This command will open your inventory."""
        await creation.Inventory.send(ctx=ctx)

    @inventory.group(name="craft", invoke_without_command=True)
    @activities.requires_game()
    @commands.max_concurrency(1, per=commands.BucketType.member, wait=False)
    async def craft(self, ctx):
        data = creation.Inventory.sendCraftables(ctx=ctx, cr_type="inv")
        await ctx.send(embed=data[0])

        if not len(data[1]):
            return

        def check(msg):
            try:
                return (0 < int(msg.content) <= len(data[1])) and (
                    ctx.author == msg.author
                )
            except:
                return False

        msg = await self.bot.wait_for("message", check=check)

        player_data = islanders.get_data_for(ctx.author)
        for ingredient, amount in data[1][int(msg.content) - 1].recipe.items():
            player_data["inventory"], success = islanders.inventory_remove(
                player_data["inventory"], ingredient, amount
            )
            if not success:
                raise OutOfItemsError(
                    f"You don't have enough {ingredient} to craft this"
                )

        player_data["inventory"], success = islanders.inventory_add(
            player_data["inventory"], data[1][int(msg.content) - 1], 1
        )
        if not success:
            return await ctx.send(
                f"You don't have enough inventory space to fit the crafted item. Put something in storage first (see `@{ctx.bot.user.name} store`)..."
            )
        islanders.write_data_for(ctx.author, player_data)

        newe = discord.Embed(
            title="Item Crafted",
            description=f"You have successfully crafted {data[1][int(msg.content)-1].name}",
            footer=f"{ctx.author}",
        )
        await ctx.send(embed=newe)

    @craft.command(name="list")
    async def craft_list(self, ctx, craftable_type="all"):
        data = creation.Inventory.sendAllCraftables(ctx=ctx, cr_type=craftable_type)
        await ctx.send(embed=data[0])

    @commands.command(name="craft", aliases=["cr"])
    @activities.requires_game()
    async def _craft(self, ctx):
        await self.craft.invoke(ctx)

    # @commands.command(name="info")
    # async def info(self, ctx):
    #     embed = discord.Embed(
    #         title=f"{ctx.author.name}'s stats: Level {}"
    #     )

    #     await ctx.send(embed=embed)

    @commands.group(
        aliases=["storage", "shared", "server"], invoke_without_command=True
    )
    @activities.requires_game()
    async def store(self, ctx):
        data = islanders.get_data_for(islanders.Server(ctx.guild))["inventory"]["items"]
        pages = commands.Paginator(prefix="**Shared Storage:**", suffix="")
        if not data:
            pages.add_line("*No items (use `store add` to store some)*")
        for item, amount in data:
            pages.add_line(f"{item}: {amount}")
        for page in pages.pages:
            await ctx.send(page)

    @commands.command(
        aliases=["🐐"], hidden=True
    )  # Hello :). I'm writing this on the last night of the competition. I think we've got most of the bugs ironed out ~~now we've only got to add the core features and we'll be done~~ -3665
    @activities.requires_game()
    async def goat(self, ctx):
        data = islanders.get_data_for(ctx.author)

        data["inventory"], success = islanders.inventory_add(
            data["inventory"], FakeItemTM("🐐"), 1
        )
        if not success:
            return await ctx.send(":goat:")
        islanders.write_data_for(ctx.author, data)

    @store.command(aliases=["+", "store", "give"])
    @activities.requires_game()
    async def add(self, ctx, amount: int, *, item):
        s_data = islanders.get_data_for(islanders.Server(ctx.guild))
        p_data = islanders.get_data_for(ctx.author)
        s_data["inventory"], _ = islanders.server_inventory_add(
            s_data["inventory"], FakeItemTM(item), amount
        )
        p_data["inventory"], success = islanders.inventory_remove(
            p_data["inventory"], FakeItemTM(item), amount
        )
        if not success:
            return await ctx.send("You don't have the stuff you're trying to store")
        islanders.write_data_for(islanders.Server(ctx.guild), s_data)
        islanders.write_data_for(ctx.author, p_data)
        await ctx.send("Successfully stored items in the shared bank")

    @store.command(aliases=["-", "get", "unstore", "take"])
    async def remove(self, ctx, amount: int, *, item):
        s_data = islanders.get_data_for(islanders.Server(ctx.guild))
        p_data = islanders.get_data_for(ctx.author)
        p_data["inventory"], space_success = islanders.inventory_add(
            p_data["inventory"], FakeItemTM(item), amount
        )
        s_data["inventory"], success = islanders.inventory_remove(
            s_data["inventory"], FakeItemTM(item), amount
        )
        if not success:
            return await ctx.send("The server doesn't have that stuff")
        if not space_success:
            return await ctx.send(
                "You don't have enough inventory space to take that stuff- try depositing some items first"
            )
        islanders.write_data_for(ctx.author, p_data)
        islanders.write_data_for(islanders.Server(ctx.guild), s_data)
        await ctx.send("Successfully took items from the shared bank")

    @commands.command(aliases=["win"])
    @activities.requires_game()
    async def sail(self, ctx):
        """Build a boat and sail away"""
        s_data = islanders.get_data_for(islanders.Server(ctx.guild))
        s_data["inventory"], success1 = islanders.inventory_remove(
            s_data["inventory"], craftables.BundledLogs, 250
        )
        s_data["inventory"], success2 = islanders.inventory_remove(
            s_data["inventory"], world.Wood, 250
        )
        s_data["inventory"], success3 = islanders.inventory_remove(
            s_data["inventory"], craftables.Sail, 5
        )
        s_data["inventory"], success4 = islanders.inventory_remove(
            s_data["inventory"], smeltables.Iron, 250
        )
        if all([success1, success2, success3, success4]):
            with open(f"data/{ctx.guild.id}.json") as data_file:
                d = json.load(data_file)
            d["active"] = False
            with open(f"data/{ctx.guild.id}.json", "w") as data_file:
                json.dump(d, data_file)
            await ctx.send(
                f"You craft a giant *goat* ||somehow I managed to spell that as *b*oat the whole time... not sure quite how? -3665|| which leaps off into the sunset carring your entire server off the island with it"
            )
            await ctx.send(
                f":tada: **YOU AND {len(d['islanders']) - 2} OTHER ISLANDERS HAVE BEAT CASTAWAY!!!** :tada: It took you guys {humanize.naturaldelta(datetime.datetime.now() - datetime.datetime.fromtimestamp(d['start_time']))}. We really hope you enjoyed playing :thumbsup:"
            )


def setup(bot):
    bot.add_cog(Castaway(bot))
