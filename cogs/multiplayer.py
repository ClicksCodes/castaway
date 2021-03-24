import discord
import humanize
import typing
import time
import json
import asyncio
import math
import os
import random

import datetime
from discord.ext import commands

from consts import *


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.assignees = "PineaFan"

    async def fetchGame(self, server, m=None, ctx=None):
        try:
            with open(f"servers/{server}.json") as f:
                return json.load(f)
        except FileNotFoundError:
            return 404
        except json.JSONDecodeError:
            if m and ctx and isinstance(server, int):
                await m.edit(embed=discord.Embed(
                    title=f"Your game seems to be broken :(",
                    description=f"Sadly, the game you have is corrupted, and there's not too much we can do.\nTo reset your island, you can `{ctx.prefix}end`.",
                    color=colours['r'],
                ))
            return 400

    async def writeGame(self, server, data, ctx=None, m=None):
        try:
            with open(f"servers/{server}.json", "w") as f:
                return json.dump(data, f, indent=2)
        except FileNotFoundError:
            if m and ctx and isinstance(server, int):
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
            if m and ctx and isinstance(server, int):
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
            with open(f"servers/{server}.json", "x") as f:
                json.dump(data, f, indent=2)
                return 201
        except FileExistsError:
            return 409
        except TypeError:
            return 400

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

    async def multiCheck(self, ctx):
        f = await self.fetchGame(ctx.guild.id)
        if not f:
            return True
        online = await self.fetchGame("MULTIPLAYER")
        if str(ctx.guild.id) not in online:
            return True
        return False

    @commands.command()
    @commands.guild_only()
    async def online(self, ctx):
        if await self.globalChecks(ctx):
            return
        game = await self.fetchGame(ctx.guild.id)
        online = await self.fetchGame("MULTIPLAYER")
        if isinstance(game, int):
            return
        if not game["settings"]["online"]:
            await ctx.reply(embed=discord.Embed(
                title="The ocean is silent",
                description=f"Your game was created in offline mode, which means you can't go online. If you want to be able to, you can `{ctx.prefix}end` and start another game",
                color=colours["o"]
            ))
        else:
            if str(ctx.guild.id) not in online.keys():
                online[str(ctx.guild.id)] = {"islandName": game["settings"]["name"], "lastSeen": 0, "requesting": []}
                await self.writeGame("MULTIPLAYER", online)
            await ctx.reply(embed=discord.Embed(
                title="Welcome aboard",
                description=f"You're online! If you want to attract passers by, you can make your smoke signal with `{ctx.prefix}smoke`",
                color=colours["g"]
            ))

    @commands.command()
    @commands.guild_only()
    async def smoke(self, ctx):
        if await self.globalChecks(ctx):
            return
        if await self.multiCheck(ctx):
            return
        game = await self.fetchGame(ctx.guild.id)
        online = await self.fetchGame("MULTIPLAYER")
        smokeTime = online[str(ctx.guild.id)]["lastSeen"]
        broadcasting = (datetime.datetime.now() - datetime.datetime.fromtimestamp(smokeTime)).total_seconds() < 60 * 60
        nearing = (datetime.datetime.now() - datetime.datetime.fromtimestamp(smokeTime)).total_seconds() > 60 * 10
        col = "r"
        if broadcasting and nearing:
            col = "o"
        elif broadcasting and not nearing:
            col = "g"
        lastSeen = ""
        if not broadcasting:
            if smokeTime == 0:
                lastSeen = "\nYou have not yet used your smoke signal"
            else:
                last = datetime.datetime.now() - datetime.datetime.fromtimestamp(smokeTime) - datetime.timedelta(seconds=60)
                lastSeen = f"\nYou were last seen {humanize.naturaldelta(last)} ago"
        else:
            last = datetime.datetime.now() - (datetime.datetime.fromtimestamp(smokeTime) + datetime.timedelta(seconds=60 * 60))
            lastSeen = f"\nYour smoke signal will last {humanize.naturaldelta(last)}"
        m = await ctx.send(embed=discord.Embed(
                title=f"{self.bot.get_emoji(emojis['smoke'][col])} Smoke",
                description=f"You are {'not ' if not broadcasting else ''}broadcasting{lastSeen}",
                color=colours[col]
            ))
        await m.add_reaction(self.bot.get_emoji(emojis["smoke"][col]))
        try:
            await ctx.bot.wait_for('reaction_add', timeout=60, check=lambda r, user: r.message.id == m.id and user == ctx.author)
        except asyncio.TimeoutError:
            return

        try:
            await m.clear_reactions()
        except Exception as e:
            print(e)

        await asyncio.sleep(0.25)

        if "campfire" in game["structures"].keys():
            if "10" not in game["players"][str(ctx.author.id)]["inventory"] or game["players"][str(ctx.author.id)]["inventory"]["10"] < 10:
                return await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(emojis['smoke']['g'])} Smoke",
                    description=f"You have no coal - It costs 10 coal to relight your campfire",
                    color=colours["g"]
                ))
            if "23" not in game["players"][str(ctx.author.id)]["inventory"]:
                return await m.edit(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(emojis['smoke']['g'])} Smoke",
                    description=f"You have no flint and steel - You need one of these in your inventory to light your campfire",
                    color=colours["g"]
                ))

            game = await self.fetchGame("MULTIPLAYER", m, ctx)
            game[str(ctx.guild.id)]["lastSeen"] = datetime.datetime.timestamp(datetime.datetime.now())
            await self.writeGame("MULTIPLAYER", game, ctx, m)

            game = await self.fetchGame(ctx.guild.id, m, ctx)
            game["players"][str(ctx.author.id)]["inventory"]["10"] -= 10
            await self.writeGame(ctx.guild.id, game, ctx, m)

            await m.edit(embed=discord.Embed(
                title=f"{self.bot.get_emoji(emojis['smoke']['g'])} Smoke",
                description=f"You are broadcasting\nYour smoke signal will last 1 hour",
                color=colours["g"]
            ))

    @commands.command()
    @commands.guild_only()
    async def search(self, ctx):
        if await self.globalChecks(ctx):
            return
        if await self.multiCheck(ctx):
            return
        online = await self.fetchGame("MULTIPLAYER")
        islands = {}
        for k, v in online.items():
            if k != str(ctx.guild.id) and ((datetime.datetime.now() - datetime.datetime.fromtimestamp(v["lastSeen"])).total_seconds() < 60 * 60):
                islands[k] = v
        coords = online[str(ctx.guild.id)]["coords"]
        desc = ""
        for island in islands.values():
            distance = round(math.sqrt((coords[0]/100-island["coords"][0]/100)**2 + (coords[1]/100-island["coords"][1]/100)**2), 2)
            desc += f"{island['islandName']} - {distance}km\n"
        await ctx.reply(embed=discord.Embed(
            title=f"Nearby islands",
            description=desc,
            color=colours["g"]
        ))


def setup(bot):
    bot.add_cog(Core(bot))
