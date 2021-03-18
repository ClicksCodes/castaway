import asyncio
import json
import os
import typing

import discord
import humanize
from consts import *
from discord.ext import commands

import items as Items


class ItemManager(commands.Cog):
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
            print(e)
            if m and ctx:
                await m.edit(embed=discord.Embed(
                    title=f"Your game seems to be broken :(",
                    description=f"Sadly, the game you have is corrupted.\nWe are going to try resetting your game with the data we tried to write.",
                    color=colours['r'],
                ))
                await asyncio.sleep(3)
                os.remove(f"servers/{server}.json")
                result = self.newGame(server, data)
                print(result)
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
        game["players"][str(user.id)]["skills"][random.choice(list(game["players"][str(user.id)]["skills"].keys()))] = 2
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

    @commands.command(aliases=["inv", "i"])
    @commands.guild_only()
    async def inventory(self, ctx, user: typing.Optional[discord.Member]):
        m = await ctx.send(embed=lembed)
        g = await self.fetchGame(ctx.guild.id, m, ctx)
        if not user:
            user = ctx.author
        if str(user.id) not in g["players"]:
            return await m.edit(embed=discord.Embed(
                title="They're not here yet :/",
                description=f"{user.display_name} is not yet on the island, get them to `{ctx.prefix}join` if you want them to join.",
                color=colours["b"]
            ))
        inventory = g["players"][str(user.id)]["inventory"]
        string = "\n".join([
            f"`{k}` {Items.items[int(k)]['name'].capitalize()}: {v}" for k, v in inventory.items()
        ])
        await m.edit(embed=discord.Embed(
            title=f"Inventory for {user.display_name}",
            description=string,
            color=colours["b"]
        ))


def setup(bot):
    bot.add_cog(ItemManager(bot))
