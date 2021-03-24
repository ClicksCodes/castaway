import discord
import json
import asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommand

from consts import *
import items as Items


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.slash = SlashCommand(bot, override_type=True, sync_commands=True)
        self.slash.slash(name='give')(self._give)

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

    async def _give(self, ctx: SlashContext, user, item, amount):
        if await self.globalChecks(ctx, ctx.author):
            return
        game = await self.fetchGame(ctx.guild.id)
        if isinstance(game, int):
            return
        if int(item) not in Items.items.keys():
            return
        if str(user.id) not in game["players"]:
            return

        if str(item) not in game["players"][str(user.id)]["inventory"]:
            game["players"][str(user.id)]["inventory"][str(item)] = amount
        else:
            game["players"][str(user.id)]["inventory"][str(item)] += amount
        await self.writeGame(ctx.guild.id, game)

        await ctx.send(embed=discord.Embed(
            title="Given",
            description=f"Gave {Items.items[int(item)]['name']} x{amount} to {user.mention}",
            color=colours["g"]
        ))


def setup(bot):
    bot.add_cog(Slash(bot))
