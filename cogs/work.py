import asyncio
import datetime
import json
import os
import typing
import random

import discord
import humanize
import items as Items
import lootTables as LootTables
from consts import *
from discord.ext import commands


class Work(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def fetchGame(self, server, m=None, ctx=None):
        try:
            with open(f"servers/{int(server)}.json") as f:
                return json.load(f)
        except FileNotFoundError:
            return 404
        except json.JSONDecodeError:
            if m and ctx:
                await m.edit(embed=discord.Embed(
                    title=f"Your game seems to be broken :(",
                    description=f"Sadly, the game you have is corrupted, and there's not too much we can do.\nTo reset your island, you can `{ctx.prefix}end`.",
                    color=colours['r'],
                ))
            return 400

    async def writeGame(self, server, data, ctx=None, m=None):
        try:
            with open(f"servers/{int(server)}.json", "w") as f:
                return json.dump(data, f, indent=2)
        except FileNotFoundError:
            if m and ctx:
                await m.edit(embed=discord.Embed(
                    title=f"Oops - Thats an error",
                    description=f"We tried to safe your game's data, but it doesn't seem to exist :/\nWe will retry by starting your game.",
                    color=colours['r'],
                ))
            await asyncio.sleep(3)
            out = self.newGame(server, data)
            if out == 200:
                return
            return 404
        except TypeError as e:
            if m and ctx:
                await m.edit(embed=discord.Embed(
                    title=f"Your game seems to be broken :(",
                    description=f"Sadly, the game you have is corrupted.\nWe are going to try resetting your game with the data we tried to write.",
                    color=colours['r'],
                ))
                await asyncio.sleep(3)
                os.remove(f"servers/{server}.json")
                result = self.newGame(server, data)
                if result == 201:
                    return 201
            return 400

    def newGame(self, server, data):
        try:
            with open(f"servers/{int(server)}.json", "x") as f:
                json.dump(data, f, indent=2)
                return 201
        except FileExistsError:
            return 409
        except TypeError:
            return 400

    async def addPlayer(self, ctx, user):
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, int):
            return
        if str(user.id) in game["players"]:
            await m.edit(embed=discord.Embed(
                title="You're already here",
                description="You are already in the game, you can't join again ;)",
                color=colours["o"]
            ))
            return
        if len(game["players"]) >= game["settings"]["max_players"] and game["settings"]["max_players"] > 0:
            await m.edit(embed=discord.Embed(
                title="The game is full",
                description="This game has got the maximum number of players allowed :/",
                color=colours["o"]
            ))
            return
        game["players"][str(user.id)] = {
            "joined": datetime.datetime.timestamp(datetime.datetime.now()),
            "hp": 10,
            "food": {
                "level": 20,
                "lastEaten": None
            },
            "water": {
                "level": 20,
                "lastDrink": None
            },
            "skills": {
                "Cooking": 0,
                "Exploring": 0,
                "Crafting": 0,
                "Scavenging": 0,
                "Fishing": 0,
                "Mining": [0, 0],
                "Farming": [0, 0]
            },
            "level": 1,
            "upgradesUsed": 0,
            "xp": 0,
            "inventory": {}
        }
        game["players"][str(user.id)]["skills"][random.choice(list(game["players"][str(user.id)]["skills"].keys()))] = [2, 0]
        await self.writeGame(ctx.guild.id, game, ctx, m)
        await m.edit(embed=discord.Embed(
            title="You're in!",
            description=f"Welcome to {game['settings']['name']}! You are player {len(game['players'])}.\n"
                        f"You can check your profile with `{ctx.prefix}profile` or manual with `{ctx.prefix}manual`",
            color=colours["g"]
        ))

    async def giveItems(self, user, server, items, ctx=None, m=None):
        game = await self.fetchGame(server)
        if isinstance(game, int):
            return
        player = game["players"][str(user)]
        inv = player["inventory"]
        for item in items:
            item = list(item)
            item[0] = str(item[0])
            if item[0] not in inv:
                game["players"][str(user)]["inventory"][item[0]] = item[1]
            else:
                game["players"][str(user)]["inventory"][item[0]] += item[1]

        return await self.writeGame(server, game, ctx, m)

    async def globalChecks(self, ctx, user=None):
        f = await self.fetchGame(ctx.guild.id)
        if f == 404:
            await ctx.send(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(emojis['Warning'])} Your server doesn't have an island",
                    description=f"You'll need to run `{ctx.prefix}start` to start up your island.",
                    color=colours["r"]
                ))
            return True
        if user:
            if str(user.id) not in f["players"]:
                await ctx.send(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(emojis['RankCard'])} {user.display_name} hasn't joined the yet",
                    description=f"{user.display_name} isn't on the island yet. Get them to run `{ctx.prefix}join` to enter the island.",
                    color=colours["r"]
                ))
                return True
        return False

    async def calcRewards(self, ctx, m):
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, int):
            return
        user = game["tasks"][str(ctx.author.id)]
        task = user["type"]
        timeTaken = (datetime.datetime.now() - datetime.datetime.fromtimestamp(user["startedAt"])).total_seconds() / 60
        level = game["players"][str(ctx.author.id)]["skills"][task.capitalize()][0] + 1
        LT = LootTables.LootTable(minutes=int(timeTaken), level=level)
        table = None
        rewardSystem = 0
        lostTile = ""
        if task == "Fishing":
            table = LootTables.fishing
            rewardSystem = 1
            if random.randint(0, 3*level) == 0:
                game["resources"]["fishing_spots"] -= 1
                lostTile = "Fishing spot"
        elif task == "Scavenging":
            table = LootTables.scavenging
            rewardSystem = 1
            if random.randint(0, 3*level) == 0:
                game["resources"]["undiscovered_land"] -= 1
                lostTile = "Undiscovered land"
        elif task == "Mining":
            table = LootTables.mining
            rewardSystem = 1
            if random.randint(0, 3*level) == 0:
                game["resources"]["mines"] -= 1
                lostTile = "Mine"
        elif task == "Farming":
            table = LootTables.farming
            rewardSystem = 1
            if random.randint(0, 3*level) == 0:
                game["resources"]["farms"] -= 1
                lostTile = "Farm"
        elif task == "Exploring":
            table = LootTables.exploring
            rewardSystem = 3
        elif task == "Cooking":
            rewardSystem = 2
        else:
            return
        levelled = False
        levelup = False
        game["players"][str(ctx.author.id)]["skills"][task][1] += int(timeTaken)
        if game["players"][str(ctx.author.id)]["skills"][task][1] > 60 * 4 * (game["players"][str(ctx.author.id)]["skills"][task][0]+1):
            levelled = True
            game["players"][str(ctx.author.id)]["skills"][task] = [game["players"][str(ctx.author.id)]["skills"][task][0]+1, 0]
        game["players"][str(ctx.author.id)]["xp"] += round(timeTaken / 10)
        while game["players"][str(ctx.author.id)]["xp"] > (game["players"][str(ctx.author.id)]["level"]*5)+5:
            levelup = True
            game["players"][str(ctx.author.id)]["xp"] -= (game["players"][str(ctx.author.id)]["level"]*5)+5
            game["players"][str(ctx.author.id)]["level"] += 1
        del game["tasks"][str(ctx.author.id)]
        await self.writeGame(ctx.guild.id, game, ctx, m)
        if rewardSystem == 1:
            collected = LT.table(LT.getTable(), table)
            collectedDict = {x: collected.count(x) for x in collected}
            itemlist = [(k, v) for k, v in collectedDict.items()]
            await self.giveItems(ctx.author.id, ctx.guild.id, itemlist, ctx, m)
        elif rewardSystem == 2:
            amount = round(LT.getTable())
            count = 0
            fromStore = []
            fromPlayer = []
            for item, props in game["store"].items():
                for _ in range(props):
                    if count >= amount:
                        break
                    count += 1
                    fromStore.append(item)
            for item, props in game["players"][str(ctx.author.id)]["inventory"].items():
                for _ in range(props):
                    if count >= amount:
                        break
                    count += 1
                    fromPlayer.append(item)

            total = 0
            for item, amount in {x: fromStore.count(x) for x in fromStore}.items():
                total += amount
                game["store"][str(item)] -= amount
                if str(item) + "1" not in game["store"]:
                    game["store"][str(item) + "1"] = amount
                else:
                    game["store"][str(item) + "1"] += amount
            for item, amount in {x: fromPlayer.count(x) for x in fromPlayer}.items():
                total += amount
                game["players"][str(ctx.author.id)]["inventory"][str(item)] -= amount
                if str(item) + "1" not in game["players"][str(ctx.author.id)]["inventory"]:
                    game["players"][str(ctx.author.id)]["inventory"][str(item) + "1"] = amount
                else:
                    game["players"][str(ctx.author.id)]["inventory"][str(item) + "1"] += amount
            await self.writeGame(ctx.guild.id, game, ctx, m)
        if rewardSystem == 3:
            collected = LT.table(LT.getTable(), table)
            game = await self.fetchGame(ctx.guild.id, m, ctx)
            if isinstance(game, int):
                return
            for r in collected:
                game["resources"][r] += 1
            await self.writeGame(ctx.guild.id, game, ctx, m)
        text = ""
        if levelled:
            text += f'\nYou also reached {task} level {game["players"][str(ctx.author.id)]["skills"][task][0]}!'
        if levelup:
            text += f'\nYou also reached player level {game["players"][str(ctx.author.id)]["level"]}!'
        if lostTile:
            text += f'\nOne {lostTile} was used up in the process.'
        if rewardSystem == 1:
            await m.edit(embed=discord.Embed(
                title=f"Finished {task}",
                description=f"You were {task} for {round(timeTaken)} minutes {text}\n"
                            f"In this time, you gathered {len(collected)}{(' ' + Items.items[list(collectedDict.keys())[0]]['name']) if len(collectedDict) == 1 else ' items'}" +
                            (f" - This includes:\n\n" if len(collectedDict) > 1 else "") +
                            ("\n".join([f"`{k}` {Items.items[int(k)]['name']}: {v}" for k, v in collectedDict.items()]) if len(collectedDict) > 1 else ""),
                color=colours["g"]
            ))
        elif rewardSystem == 2:
            await m.edit(embed=discord.Embed(
                title=f"Finished {task}",
                description=f"You were {task} for {round(timeTaken)} minutes {text}\n"
                            f"In this time, {total} items were cooked and added back to your store/inventory",
                color=colours["g"]
            ))
        elif rewardSystem == 3:
            await m.edit(embed=discord.Embed(
                title=f"Finished {task}",
                description=f"You were {task} for {round(timeTaken)} minutes {text}\n"
                            f"In this time, {len(collected)} places were discovered - you can see them in `{ctx.prefix}places`",
                color=colours["g"]
            ))
        await asyncio.sleep(1)

    async def startTask(self, ctx, m, task):
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, int):
            return
        taskplaces = {
            "Fishing": "fishing_spots",
            "Mining": "mines",
            "Scavenging": "undiscovered_land",
            "Farming": "farms"
        }
        if task in taskplaces.keys():
            if game["resources"][taskplaces[task]] == 0:
                return await ctx.reply(embed=discord.Embed(
                    title=f"Theres nowhere to go {task}",
                    description=f"You tried to go {task}, but there was nowhere to go :/\n"
                                f"Someone will have to go exploring (`{ctx.prefix}explore`) to find new areas to go {task}.\n"
                                f"View your current locations with `{ctx.prefix}places`",
                    color=colours["g"]
                ))
        game["tasks"][str(ctx.author.id)] = {"type": task, "startedAt": datetime.datetime.timestamp(datetime.datetime.now())}
        await self.writeGame(ctx.guild.id, game, ctx, m)
        if isinstance(game, int):
            return
        await ctx.reply(embed=discord.Embed(
            title=f"You have started {task}",
            description=f"Do `{ctx.prefix}stop` or start another task to collect your rewards, but it will take some time",
            color=colours["g"]
        ))

    @commands.command()
    async def cook(self, ctx):
        if await self.globalChecks(ctx, user=ctx.author):
            return
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, int):
            return
        if str(ctx.author.id) in game["tasks"]:
            await self.calcRewards(ctx, m)
        await self.startTask(ctx, m, "Cooking")

    @commands.command()
    async def explore(self, ctx):
        if await self.globalChecks(ctx, user=ctx.author):
            return
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if str(ctx.author.id) in game["tasks"]:
            await self.calcRewards(ctx, m)
        await self.startTask(ctx, m, "Exploring")

    @commands.command(aliases=["collect"])
    async def scavenge(self, ctx):
        if await self.globalChecks(ctx, user=ctx.author):
            return
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, int):
            return
        if str(ctx.author.id) in game["tasks"]:
            await self.calcRewards(ctx, m)
        await self.startTask(ctx, m, "Scavenging")

    @commands.command()
    async def fish(self, ctx):
        if await self.globalChecks(ctx, user=ctx.author):
            return
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, int):
            return
        if str(ctx.author.id) in game["tasks"]:
            await self.calcRewards(ctx, m)
        await self.startTask(ctx, m, "Fishing")

    @commands.command()
    async def mine(self, ctx):
        if await self.globalChecks(ctx, user=ctx.author):
            return
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, int):
            return
        if str(ctx.author.id) in game["tasks"]:
            await self.calcRewards(ctx, m)
        await self.startTask(ctx, m, "Mining")

    @commands.command()
    async def farm(self, ctx):
        if await self.globalChecks(ctx, user=ctx.author):
            return
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, int):
            return
        if str(ctx.author.id) in game["tasks"]:
            await self.calcRewards(ctx, m)
        await self.startTask(ctx, m, "Farming")

    @commands.command(aliases=["cancel"])
    async def stop(self, ctx):
        if await self.globalChecks(ctx, user=ctx.author):
            return
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, int):
            return
        if str(ctx.author.id) in game["tasks"]:
            await self.calcRewards(ctx, m)
        else:
            await m.edit(embed=discord.Embed(
                title="Nothing to do",
                description="You weren't doing any tasks :(",
                color=colours["o"]
            ))

    @commands.command()
    @commands.guild_only()
    async def places(self, ctx):
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, int):
            return
        await m.edit(embed=discord.Embed(
            title="Discovered places",
            description=f"{self.bot.get_emoji(emojis['Fishing'])    } Fishing spots: {game['resources']['fishing_spots']}\n"
                        f"{self.bot.get_emoji(emojis['Scavenging']) } Undiscovered land: {game['resources']['undiscovered_land']}\n"
                        f"{self.bot.get_emoji(emojis['Farming'])    } Farms: {game['resources']['farms']}\n"
                        f"{self.bot.get_emoji(emojis['Mining'])     } Mines: {game['resources']['mines']}",
            color=colours["b"]
        ))

    @commands.command()
    @commands.guild_only()
    async def tasks(self, ctx):
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, int):
            return
        await m.edit(embed=discord.Embed(
            title="Current active tasks",
            description="\n".join([f"{ctx.guild.get_member(int(k)).mention}: {v['type']}" for k, v in game["tasks"].items()]),
            color=colours["b"]
        ))


def setup(bot):
    bot.add_cog(Work(bot))
