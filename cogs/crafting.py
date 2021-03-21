import asyncio
import json
import os
import datetime
import typing

import discord
import humanize
from consts import *
from discord.ext import commands

import items as Items


class Crafting(commands.Cog):
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

    async def craftItem(self, ctx, m, user, server, item):
        game = await self.fetchGame(server)
        if isinstance(game, int):
            return
        if str(ctx.author.id) in game["tasks"]:
            await m.edit(embed=discord.Embed(
                title=f"Already {game['tasks'][str(ctx.author.id)]['type']}",
                description=f"You need to `{ctx.prefix}stop` before you can craft",
                color=colours["r"]
            ))
            await asyncio.sleep(5)
            return
        limits = []
        ingredients = [(k, v) for k, v in Items.items[item]["recipe"]["in"].items()]
        inventory = game["players"][str(user)]["inventory"]
        usefulInv = {}
        for i in Items.items[item]["recipe"]["in"].keys():
            if str(i) not in inventory:
                limits.append(i)
                continue
            usefulInv[str(i)] = int(game["players"][str(user)]["inventory"][str(i)])
        if len(limits):
            await m.edit(embed=discord.Embed(
                title="Not enough resources",
                description=f"You do not have any of the following resources: {', '.join([Items.items[limit]['name'] for limit in limits])}",
                color=colours["r"]
            ))
            await asyncio.sleep(5)
            return
        if "max" in Items.items[item]["recipe"]:
            limit = Items.items[item]["recipe"]["max"]
            amount = Items.items[item]["recipe"]["max"]
            forRec = [[str(k), int(v)] for k, v in Items.items[item]["recipe"]["in"].items()]
        else:
            limit = 0
            forRec = [[str(k), int(v)] for k, v in Items.items[item]["recipe"]["in"].items()]
            br = False
            while limit < 1000:
                for i in forRec:
                    usefulInv[i[0]] -= i[1]
                for _, v in usefulInv.items():
                    if v < 0:
                        br = True
                        break
                if br:
                    break
                limit += 1
            time = (Items.items[item]["recipe"]["time"]*limit) / (game["players"][str(user)]["skills"]["Crafting"][0] + 1)
            await m.add_reaction(self.bot.get_emoji(emojis["cross"]))
            n = ', '.join([f'{Items.items[i[0]]["name"]} x{i[1]}' for i in ingredients])
            await m.edit(embed=discord.Embed(
                title="How many do you want to make?",
                description=f"You can make {Items.items[int(item)]['name']} x{limit * Items.items[item]['recipe']['out']} in "
                            f"{round(time, 2)}s ({humanize.naturaldelta(datetime.timedelta(seconds=time))})\n"
                            f"It costs {n} to make {Items.items[item]['recipe']['out']} {Items.items[item]['name']} at "
                            f"{Items.items[item]['recipe']['out']} items / {Items.items[item]['recipe']['time']}s",
                color=colours["g"]
            ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: Number"))

            try:
                done, _ = await asyncio.wait([
                    ctx.bot.wait_for('message', timeout=120, check=lambda message: message.author == ctx.author),
                    ctx.bot.wait_for('reaction_add', timeout=120, check=lambda _, user: user == ctx.author)
                ], return_when=asyncio.FIRST_COMPLETED)
            except asyncio.TimeoutError:
                return

            await m.clear_reactions()

            response = done.pop().result()
            if type(response) == discord.message.Message:
                await response.delete()
                try:
                    amount = round(int(response.content) / Items.items[item]['recipe']['out'])
                    if amount > limit:
                        amount = limit
                    if amount < 1:
                        amount = 1
                except ValueError:
                    return
            else:
                return
            for future in done:
                future.exception()
        await m.edit(embed=discord.Embed(
            title="Crafting",
            description=f"You are now making {Items.items[int(item)]['name']} x{amount * Items.items[item]['recipe']['out']}...",
            color=colours["g"]
        ))
        game = await self.fetchGame(server, m, ctx)
        game["tasks"][str(ctx.author.id)] = {"type": "Crafting", "startedAt": datetime.datetime.timestamp(datetime.datetime.now())}
        await self.writeGame(server, game, ctx, m)
        timeMultiplier = Items.Multiplier(item, game["storeSize"]).timeMultiplier()
        await asyncio.sleep((Items.items[item]["recipe"]["time"]*amount*timeMultiplier) / (game["players"][str(user)]["skills"]["Crafting"][0] + 1))
        game = await self.fetchGame(server, m, ctx)
        multiplier = Items.Multiplier(item, game["storeSize"]).itemMultiplier()
        if str(ctx.author.id) not in game["tasks"]:
            return
        if game["tasks"][str(ctx.author.id)]["type"] != "Crafting":
            return
        del game["tasks"][str(ctx.author.id)]
        for i in forRec:
            game["players"][str(ctx.author.id)]["inventory"][i[0]] -= i[1] * amount * multiplier
            if game["players"][str(ctx.author.id)]["inventory"][i[0]] <= 0:
                del game["players"][str(ctx.author.id)]["inventory"][i[0]]
        if int(item) == 50:
            game["storeSize"] += 1
        else:
            if str(item) in game["players"][str(ctx.author.id)]["inventory"]:
                game["players"][str(ctx.author.id)]["inventory"][str(item)] += amount * Items.items[item]['recipe']['out']
            else:
                game["players"][str(ctx.author.id)]["inventory"][str(item)] = amount * Items.items[item]['recipe']['out']
        await self.writeGame(server, game, ctx, m)
        await m.edit(embed=discord.Embed(
            title="Crafting",
            description=f"You made {Items.items[int(item)]['name']} x{amount * Items.items[item]['recipe']['out']}",
            color=colours["g"]
        ))
        await asyncio.sleep(3)

    @commands.command(aliases=["c", "crafting"])
    @commands.guild_only()
    async def craft(self, ctx, iid: typing.Optional[int]):
        if await self.globalChecks(ctx, ctx.author):
            return
        keys = {
            0: "Collected items",
            1: "Ores and metals",
            2: "Materials",
            3: "Materials",
            4: "Foodstuffs",
            5: "Structures",
            6: "Structures"
        }
        craftables = {k: [] for k in keys.keys()}
        for k, v in Items.items.items():
            if len(str(k)) == 1:
                k = f"0{k}"
            heading = int(str(k)[0])
            d = v
            d['iid'] = int(k)
            craftables[heading].append(d)
        page = 0
        m = await ctx.send(embed=lembed)
        if iid:
            if iid not in Items.items.keys():
                return
            await self.craftItem(ctx, m, ctx.author.id, ctx.guild.id, iid)
            return
        for r in [emojis['left'], emojis['right'], emojis['cross']]:
            await m.add_reaction(self.bot.get_emoji(r))
        game = await self.fetchGame(ctx.guild.id)
        while True:
            string = []
            for item in craftables[page]:
                current = f"`{item['iid']}` "
                current += f"**{item['name'].capitalize()}** "
                if "recipe" in item:
                    current += "- Recipe: `"
                    multiplier = Items.Multiplier(item['iid'], game["storeSize"]).itemMultiplier()
                    timeMultiplier = Items.Multiplier(item['iid'], game["storeSize"]).timeMultiplier()
                    current += ", ".join([f"{Items.items[k]['name']} x{v * multiplier}" for k, v in item["recipe"]["in"].items()])
                    current += f"` -> {item['recipe']['out']} {item['name'].capitalize()} (in {item['recipe']['time'] * timeMultiplier}s)"
                else:
                    current += "- *Not craftable*"
                string.append(current)
            string = "\n".join(string)
            await m.edit(embed=discord.Embed(
                title=f"Crafting: {keys[page]} ({page+1}/{len(keys.keys())})",
                description=f"Enter an item ID to craft it | Do `{ctx.prefix}item` for info on an item\n\n" + string,
                color=colours['b']
            ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: Number"))
            try:
                done, _ = await asyncio.wait([
                    ctx.bot.wait_for('message', timeout=120, check=lambda message: message.author == ctx.author),
                    ctx.bot.wait_for('reaction_add', timeout=120, check=lambda _, user: user == ctx.author)
                ], return_when=asyncio.FIRST_COMPLETED)
            except asyncio.TimeoutError:
                break

            try:
                response = done.pop().result()
                if type(response) == discord.message.Message:
                    try:
                        item = int(response.content)
                        if item not in Items.items.keys():
                            continue
                        await response.delete()
                        await self.craftItem(ctx, m, ctx.author.id, ctx.guild.id, item)
                    except ValueError:
                        continue
                else:
                    await m.remove_reaction(response[0].emoji, ctx.author)
                    if response[0].emoji.name == "cross":
                        break
                    elif response[0].emoji.name == "left":
                        page -= 1
                    else:
                        page += 1
                    page = min(max(0, page), len(keys.keys()))
            except Exception as e:
                print(e)
            for future in done:
                future.exception()
        await asyncio.sleep(0.8)
        await m.clear_reactions()

    @commands.command()
    @commands.guild_only()
    async def item(self, ctx, item: typing.Optional[str]):
        if await self.globalChecks(ctx):
            return
        if not item:
            return await ctx.reply(embed=discord.Embed(
                title=f"Which item?",
                description=f"You need to enter an item ID to show info for",
                color=colours['r']
            ))
        try:
            iid = item
            item = Items.items[int(item)]
        except (TypeError, KeyError):
            return await ctx.reply(embed=discord.Embed(
                title=f"I don't know that item",
                description=f"I couldn't find an item with that ID",
                color=colours['r']
            ))
        game = await self.fetchGame(ctx.guild.id)
        recipe = ""
        if "recipe" in item:
            recipe = "Recipe - `"
            ex = ""
            multiplier = Items.Multiplier(iid, game["storeSize"]).itemMultiplier()
            timeMultiplier = Items.Multiplier(iid, game["storeSize"]).timeMultiplier()
            if int(iid) == 50:
                ex = f"\nUpgrades to level {game['storeSize']+1}, {((game['storeSize']+1)**2)*100} item capacity"
            recipe += ", ".join([f"{Items.items[int(k)]['name']} x{v * multiplier}" for k, v in item['recipe']['in'].items()])
            recipe += f"` -> {item['recipe']['out']} {item['name'].capitalize()} (in {item['recipe']['time'] * timeMultiplier}s) {ex}"
        else:
            recipe = "*Not craftable*"
        await ctx.reply(embed=discord.Embed(
            title=f"{item['name']}",
            description=f"{item['description']}\n"
                        f"{recipe}\n"
                        f"Found by: {item['found']}",
            color=colours['b']
        ))


def setup(bot):
    bot.add_cog(Crafting(bot))
