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

    @commands.command(aliases=["inv", "i"])
    @commands.guild_only()
    async def inventory(self, ctx, user: typing.Optional[discord.Member]):
        if await self.globalChecks(ctx, (user or ctx.author)):
            return
        m = await ctx.send(embed=lembed)
        g = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(g, int):
            return
        if not user:
            user = ctx.author
        if str(user.id) not in g["players"]:
            return await m.edit(embed=discord.Embed(
                title="They're not here yet :/",
                description=f"{user.display_name} is not yet on the island, get them to `{ctx.prefix}join` if you want them to join.",
                color=colours["b"]
            ))
        if user.id != ctx.author.id:
            inventory = g["players"][str(user.id)]["inventory"]
            string = "\n".join([
                f"`{k}` {Items.items[int(k)]['name'].capitalize()}: {v}" for k, v in inventory.items()
            ])
            await m.edit(embed=discord.Embed(
                title=f"Inventory for {user.display_name}",
                description=string,
                color=colours["b"]
            ))
        if user.id == ctx.author.id:
            while True:
                g = await self.fetchGame(ctx.guild.id, m, ctx)
                inventory = g["players"][str(user.id)]["inventory"]
                string = "\n".join([
                    f"`{k}` {Items.items[int(k)]['name'].capitalize()}: {v}" for k, v in inventory.items()
                ])
                s = f"{self.bot.get_emoji(emojis['Transfer'])} Transfer items to store | {self.bot.get_emoji(emojis['Delete'])} Destroy items | " \
                    f"{self.bot.get_emoji(emojis['Sort'])} Sort items\n\n" + string
                await m.edit(embed=discord.Embed(
                    title=f"Inventory for {user.display_name}",
                    description=s,
                    color=colours["b"]
                ).set_footer(text=f"I'm listening for your next reaction, {ctx.author.display_name} | Expected: Reaction"))
                await m.add_reaction(self.bot.get_emoji(emojis["Transfer"]))
                await m.add_reaction(self.bot.get_emoji(emojis["Delete"]))
                await m.add_reaction(self.bot.get_emoji(emojis["Sort"]))

                try:
                    reaction = await ctx.bot.wait_for('reaction_add', timeout=60, check=lambda r, user: r.message.id == m.id and user == ctx.author)
                except asyncio.TimeoutError:
                    break

                try:
                    await m.remove_reaction(reaction[0].emoji, ctx.author)
                except Exception as e:
                    print(e)
                r = reaction[0].emoji.name.lower()

                if r in ["delete", "transfer"]:
                    deleting = (r == "delete")
                    if deleting:
                        s = f"Send the item IDs of the items you wish to destroy, separated by spaces, or \"all\" to destroy everything. " \
                            f"React with {self.bot.get_emoji(emojis['Delete'])} to cancel\n\n" + string
                        await m.edit(embed=discord.Embed(
                            title=f"{self.bot.get_emoji(emojis['Delete'])} Destroy items",
                            description=s,
                            color=colours["r"]
                        ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: Number, list"))
                    else:
                        s = f"Send the item IDs of the items you wish to move to the store, separated by spaces, or \"all\" to transfer everything. React with " \
                            f"{self.bot.get_emoji(emojis['Delete'])} to cancel\n\n" + string
                        await m.edit(embed=discord.Embed(
                            title=f"{self.bot.get_emoji(emojis['Transfer'])} Transfer items",
                            description=s,
                            color=colours["o"]
                        ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: Number, list"))
                    await m.remove_reaction(self.bot.get_emoji(emojis["Transfer"]), ctx.me)
                    await m.remove_reaction(self.bot.get_emoji(emojis["Sort"]), ctx.me)
                    try:
                        done, _ = await asyncio.wait([
                            ctx.bot.wait_for('message', timeout=120, check=lambda message: message.author == ctx.author),
                            ctx.bot.wait_for('reaction_add', timeout=120, check=lambda _, user: user == ctx.author)
                        ], return_when=asyncio.FIRST_COMPLETED)
                    except asyncio.TimeoutError:
                        break

                    try:
                        text = None
                        response = done.pop().result()
                        if type(response) == discord.message.Message:
                            await response.delete()
                            g = await self.fetchGame(ctx.guild.id, m, ctx)
                            if response.content.lower() == "all":
                                for item in g["players"][str(ctx.author.id)]["inventory"].copy().keys():
                                    try:
                                        if not deleting:
                                            amount = int(g["players"][str(ctx.author.id)]["inventory"][str(item)])
                                            if item not in g["store"]:
                                                g["store"][item] = amount
                                            else:
                                                g["store"][item] += amount
                                        del g["players"][str(ctx.author.id)]["inventory"][str(item)]
                                    except KeyError:
                                        pass
                            else:
                                for item in response.content.split(" "):
                                    try:
                                        if not deleting:
                                            amount = int(g["players"][str(ctx.author.id)]["inventory"][str(item)])
                                            if item not in g["store"]:
                                                g["store"][item] = amount
                                            else:
                                                g["store"][item] += amount
                                        del g["players"][str(ctx.author.id)]["inventory"][str(item)]
                                    except KeyError:
                                        pass
                            if sum([v for k, v in g["store"].items()]) > (g["storeSize"]**2) * 100:
                                await m.edit(embed=discord.Embed(
                                    title=f"Inventory",
                                    description=f"The community store is full - Adding these items would take it over its capacity of {(g['storeSize']**2)*100} items",
                                    color=colours["r"]
                                ))
                                await asyncio.sleep(5)
                            else:
                                await self.writeGame(ctx.guild.id, g, ctx, m)
                        else:
                            pass
                        await m.clear_reactions()
                    except Exception as e:
                        print(e)
                    for future in done:
                        future.exception()
                elif r in ["sort"]:
                    g = await self.fetchGame(ctx.guild.id, m, ctx)
                    inv = g["players"][str(ctx.author.id)]["inventory"]
                    tuples = [(k, v) for k, v in inv.items()]
                    tuples = sorted(tuples, key=lambda x: int(x[0]))
                    g["players"][str(ctx.author.id)]["inventory"] = {i[0]: i[1] for i in tuples}
                    await self.writeGame(ctx.guild.id, g, ctx, m)
            await m.clear_reactions()

    @commands.command(aliases=["s"])
    @commands.guild_only()
    async def store(self, ctx):
        if await self.globalChecks(ctx):
            return
        m = await ctx.send(embed=lembed)
        g = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(g, int):
            return
        await m.add_reaction(self.bot.get_emoji(emojis["Sort"]))
        await m.add_reaction(self.bot.get_emoji(emojis["Transfer"]))
        while True:
            store = g["store"]
            string = "\n".join([
                f"`{k}` {Items.items[int(k)]['name'].capitalize()}: {v}" for k, v in store.items()
            ])
            s = f"{self.bot.get_emoji(emojis['Sort'])} Sort items | {self.bot.get_emoji(emojis['Transfer'])} Transfer items\n" \
                f"{sum([v for k, v in g['store'].items()])} used of {(g['storeSize']**2)*100}\n\n" + string
            await m.edit(embed=discord.Embed(
                title=f"Community store",
                description=s,
                color=colours["b"]
            ).set_footer(text=f"I'm listening for your next reaction, {ctx.author.display_name} | Expected: Reaction"))
            try:
                reaction = await ctx.bot.wait_for('reaction_add', timeout=60, check=lambda r, user: r.message.id == m.id and user == ctx.author)
            except asyncio.TimeoutError:
                break

            try:
                await m.remove_reaction(reaction[0].emoji, ctx.author)
            except Exception as e:
                print(e)
            r = reaction[0].emoji.name.lower()

            if r == "sort":
                g = await self.fetchGame(ctx.guild.id, m, ctx)
                inv = g["store"]
                tuples = [(k, v) for k, v in inv.items()]
                tuples = sorted(tuples, key=lambda x: int(x[0]))
                g["store"] = {i[0]: i[1] for i in tuples}
                await self.writeGame(ctx.guild.id, g, ctx, m)
            elif r == "transfer":
                s = f"Send the item IDs of the items you wish to move to your inventory, separated by spaces. React with " \
                    f"{self.bot.get_emoji(emojis['Delete'])} to cancel\n\n" + string
                await m.edit(embed=discord.Embed(
                    title=f"Community store",
                    description=s,
                    color=colours["o"]
                ).set_footer(text=f"I'm listening for your next reaction, {ctx.author.display_name} | Expected: Reaction"))
                await m.remove_reaction(self.bot.get_emoji(emojis["Transfer"]), ctx.me)
                await asyncio.sleep(0.08)
                await m.remove_reaction(self.bot.get_emoji(emojis["Sort"]), ctx.me)
                await asyncio.sleep(0.08)
                await m.add_reaction(self.bot.get_emoji(emojis["Delete"]))
                try:
                    done, _ = await asyncio.wait([
                        ctx.bot.wait_for('message', timeout=120, check=lambda message: message.author == ctx.author),
                        ctx.bot.wait_for('reaction_add', timeout=120, check=lambda _, user: user == ctx.author)
                    ], return_when=asyncio.FIRST_COMPLETED)
                except asyncio.TimeoutError:
                    break

                try:
                    text = None
                    response = done.pop().result()
                    if type(response) == discord.message.Message:
                        await response.delete()
                        g = await self.fetchGame(ctx.guild.id, m, ctx)
                        for item in response.content.split(" "):
                            try:
                                amount = int(g["store"][str(item)])
                                if item not in g["players"][str(ctx.author.id)]["inventory"]:
                                    g["players"][str(ctx.author.id)]["inventory"][str(item)] = amount
                                else:
                                    g["players"][str(ctx.author.id)]["inventory"][str(item)] += amount
                                del g["store"][str(item)]
                            except KeyError:
                                pass
                        await self.writeGame(ctx.guild.id, g, ctx, m)
                    else:
                        pass
                    await m.clear_reactions()
                except Exception as e:
                    print(e)
                for future in done:
                    future.exception()
                await m.clear_reactions()
                await asyncio.sleep(0.08)
                await m.add_reaction(self.bot.get_emoji(emojis["Sort"]))
                await asyncio.sleep(0.08)
                await m.add_reaction(self.bot.get_emoji(emojis["Transfer"]))
        await m.clear_reactions()


def setup(bot):
    bot.add_cog(ItemManager(bot))
