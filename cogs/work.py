import asyncio
import datetime
import json
import os
import typing

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
        if str(user.id) in game["players"]:
            await m.edit(embed=discord.Embed(
                title="You're already here",
                description="You are already in the game, you can't join again ;)",
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
        user = game["tasks"][str(ctx.author.id)]
        task = user["type"]
        timeTaken = (datetime.datetime.now() - datetime.datetime.fromtimestamp(user["startedAt"])).total_seconds() / 60
        LT = LootTables.LootTable(minutes=int(timeTaken), level=game["players"][str(ctx.author.id)]["skills"][task.capitalize()][0]+1)
        table = None
        if task == "Fishing":
            table = LootTables.fishing
        elif task == "Scavenging":
            table = LootTables.scavenging
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
        collected = LT.table(LT.getTable(), table)
        collectedDict = {x: collected.count(x) for x in collected}
        itemlist = [(k, v) for k, v in collectedDict.items()]
        await self.giveItems(ctx.author.id, ctx.guild.id, itemlist, ctx, m)
        text = ""
        if levelled:
            text += f'\nYou also reached {task} level {game["players"][str(ctx.author.id)]["skills"][task][0]}!'
        if levelup:
            text += f'\nYou also reached player level {game["players"][str(ctx.author.id)]["level"]}!'
        await m.edit(embed=discord.Embed(
            title=f"Finished {task}",
            description=f"You were {task} for {round(timeTaken)} minutes {text}\n"
                        f"In this time, you gathered {len(collected)}{(' ' + Items.items[list(collectedDict.keys())[0]]['name']) if len(collectedDict) == 1 else ' items'}" +
                        (f" - This includes:\n\n" if len(collectedDict) > 1 else "") +
                        ("\n".join([f"`{k}` {Items.items[int(k)]['name']}: {v}" for k, v in collectedDict.items()]) if len(collectedDict) > 1 else ""),
            color=colours["g"]
        ))
        await asyncio.sleep(5)

    async def startTask(self, ctx, m, task):
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, int):
            return
        game["tasks"][str(ctx.author.id)] = {"type": task, "startedAt": datetime.datetime.timestamp(datetime.datetime.now())}
        await self.writeGame(ctx.guild.id, game, ctx, m)
        if isinstance(game, int):
            return
        await m.edit(embed=discord.Embed(
            title=f"You have started {task}",
            description=f"Do `{ctx.prefix}stop` or another task to collect your rewards, but it will take some time",
            color=colours["g"]
        ))

    @commands.command()
    async def cook(self, ctx):
        if await self.globalChecks(ctx, user=ctx.author):
            return
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
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
        if str(ctx.author.id) in game["tasks"]:
            await self.calcRewards(ctx, m)
        await self.startTask(ctx, m, "Scavenging")

    @commands.command()
    async def fish(self, ctx):
        if await self.globalChecks(ctx, user=ctx.author):
            return
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if str(ctx.author.id) in game["tasks"]:
            await self.calcRewards(ctx, m)
        await self.startTask(ctx, m, "Fishing")

    @commands.command(aliases=["cancel"])
    async def stop(self, ctx):
        if await self.globalChecks(ctx, user=ctx.author):
            return
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
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
    async def debug(self, ctx):
        if await self.globalChecks(ctx, ctx.author):
            return
        await self.giveItems(ctx.author.id, ctx.guild.id, [(0, 10), (1, 20)])


def setup(bot):
    bot.add_cog(Work(bot))
