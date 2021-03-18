import asyncio
import datetime
import io
import json
import math
import os
import random
import typing

import discord
import humanize
from consts import *
from discord.ext import commands

from . import world


class Castaway(commands.Cog):
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
                "Cooking": [0, 0],
                "Exploring": [0, 0],
                "Crafting": [0, 0],
                "Scavenging": [0, 0],
                "Fishing": [0, 0]
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

    @commands.command()
    @commands.guild_only()
    async def start(self, ctx):
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, dict):
            return await m.edit(embed=discord.Embed(
                title=f"{self.bot.get_emoji(emojis['Warning'])} Your server has already started",
                description=f"If you want to restart your island, you can run `{ctx.prefix}restart` to start your island over.",
                color=colours["r"]
            ))
        if game != 404:
            return
        options = {
            "name": "Castaway Island",
            "max_players": 0,
            "size": (25, 25),
            "seed": random.randint(0, 100000000),
            "difficulty": 2,
            "online": False
        }
        for _ in range(0, 50):
            diffstring = 'Easy' if options['difficulty'] == 1 else 'Normal' if options['difficulty'] == 2 else 'Hard'
            await m.edit(embed=discord.Embed(
                title="Island setup",
                description=f"{self.bot.get_emoji(emojis['Name'])                              } **Name:** {options['name']}\n"
                            f"{self.bot.get_emoji(emojis['Max_Players'])                       } **Max Players:** {options['max_players']}\n"
                            f"{self.bot.get_emoji(emojis['Size'])                              } **Size:** {options['size'][0]}x{options['size'][1]}\n"
                            f"{self.bot.get_emoji(emojis['Seed'])                              } **Seed:** `{options['seed']}`\n"
                            f"{self.bot.get_emoji(emojis['Difficulty'][options['difficulty']]) } **Difficulty:** {diffstring}\n"
                            f"{self.bot.get_emoji(emojis['Online'][int(options['online'])])    } **Online:** {'Yes' if options['online'] else 'No'}",
                color=colours["b"]
            ))
            for r in [
                791683415131815946, 791683553741111336, 794172731356348417,
                794172731381252096, 794172731708932116, 794172731439579188,
                794172731708932116, 794172731032993793, 794172731473002536
            ]:
                await m.add_reaction(self.bot.get_emoji(r))

            reaction = None
            try:
                reaction = await ctx.bot.wait_for('reaction_add', timeout=60, check=lambda r, user: r.message.id == m.id and user == ctx.author)
            except asyncio.TimeoutError:
                break

            try:
                await m.remove_reaction(reaction[0].emoji, ctx.author)
            except Exception as e:
                print(e)
            r = reaction[0].emoji

            await asyncio.sleep(0.25)

            if r.name == "tick":
                await m.clear_reactions()
                await m.edit(embed=discord.Embed(
                    title=f"Hang tight",
                    description="Please wait while we set up your game. This could take some time",
                    color=colours['b'],
                ))
                defaultGame = {
                    "players": {},
                    "tasks": {},
                    "settings": options,
                    "store": {}
                }
                out = self.newGame(ctx.guild.id, defaultGame)
                if out == 201:
                    await m.edit(embed=discord.Embed(
                        title=f"You're all set!",
                        description=f"Your island was created! You can check your `{ctx.prefix}profile`, and get your friends to `{ctx.prefix}join`.",
                        color=colours['g'],
                    ))
                elif out == 409:
                    await m.edit(embed=discord.Embed(
                        title=f"How'd you do that?",
                        description=f"You started a game, but it already exists :/\nIf you want to end your game, you can always `{ctx.prefix}end`.",
                        color=colours['o'],
                    ))

                return

            elif r.name == "cross":
                break
            elif r.name == "Name":
                await m.clear_reactions()
                await m.edit(
                    embed=discord.Embed(
                        title=f"{self.bot.get_emoji(emojis['Name'])} What should the island be called?",
                        description="Please enter a name for the island. Type `cancel` to cancel.",
                        color=colours['r'],
                    ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: `Text`")
                )
                try:
                    msg = await ctx.bot.wait_for('message', timeout=120, check=lambda message: message.author == ctx.author)
                except asyncio.TimeoutError:
                    break
                await msg.delete()
                if msg.content.lower() != "cancel":
                    options['name'] = msg.content[:100]
            elif r.name == "Max_Players":
                await m.clear_reactions()
                await m.edit(
                    embed=discord.Embed(
                        title=f"{self.bot.get_emoji(emojis['Max_Players'])} How many people should be allowed on the island?",
                        description="Please enter the limit of people on the island. 0 means no limit. Type `cancel` to cancel.",
                        color=colours['o'],
                    ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: `Number`")
                )
                try:
                    msg = await ctx.bot.wait_for('message', timeout=120, check=lambda message: message.author == ctx.author)
                except asyncio.TimeoutError:
                    break
                await msg.delete()
                if msg.content.lower() != "cancel":
                    try:
                        msgc = int(msg.content)
                        if msgc < 1000 and msgc >= 0:
                            options['max_players'] = msgc
                    except ValueError:
                        continue
            elif r.name == "Size":
                await m.clear_reactions()
                await m.edit(
                    embed=discord.Embed(
                        title=f"{self.bot.get_emoji(emojis['Size'])} How big should your island be?",
                        description="Please enter the size of your island. Default is 25, limit is 6-100. Type `cancel` to cancel.",
                        color=colours['g'],
                    ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: `Number`")
                )
                try:
                    msg = await ctx.bot.wait_for('message', timeout=120, check=lambda message: message.author == ctx.author)
                except asyncio.TimeoutError:
                    break
                await msg.delete()
                if msg.content.lower() != "cancel":
                    try:
                        msgc = int(msg.content)
                        if msgc < 101 and msgc > 5:
                            options['size'] = (msgc, msgc)
                    except ValueError:
                        continue
            elif r.name == "Seed":
                await m.clear_reactions()
                await m.edit(
                    embed=discord.Embed(
                        title=f"{self.bot.get_emoji(emojis['Seed'])} What should your island seed be?",
                        description="This is the number used to generate your island. Limit is 0-1 billion. Type `cancel` to cancel.",
                        color=colours['g'],
                    ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: `Number`")
                )
                try:
                    msg = await ctx.bot.wait_for('message', timeout=120, check=lambda message: message.author == ctx.author)
                except asyncio.TimeoutError:
                    break
                await msg.delete()
                if msg.content.lower() != "cancel":
                    try:
                        msgc = int(msg.content)
                        if msgc < 1000000001 and msgc >= 0:
                            options['seed'] = msgc
                    except ValueError:
                        continue
            elif r.name == "Difficulty2":
                await m.clear_reactions()
                await m.edit(
                    embed=discord.Embed(
                        title=f"{self.bot.get_emoji(emojis['Difficulty'][2])} What should your game difficulty be?",
                        description="What should your game difficulty be. 1 is easy, 2 is normal, and 3 is hard. Type `cancel` to cancel.",
                        color=colours['C'],
                    ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: `Number`")
                )
                try:
                    msg = await ctx.bot.wait_for('message', timeout=120, check=lambda message: message.author == ctx.author)
                except asyncio.TimeoutError:
                    break
                await msg.delete()
                if msg.content.lower() != "cancel":
                    try:
                        msgc = int(msg.content)
                        if msgc < 4 and msgc >= 1:
                            options['difficulty'] = msgc
                    except ValueError:
                        continue
            elif r.name == "Online1":
                await m.clear_reactions()
                await m.edit(
                    embed=discord.Embed(
                        title=f"{self.bot.get_emoji(emojis['Name'])} Want to play online?",
                        description="Enter `y` or `n` to choose if you want to interact with other islands for trading. Type `cancel` to cancel.",
                        color=colours['C'],
                    ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: `Text`")
                )
                try:
                    msg = await ctx.bot.wait_for('message', timeout=120, check=lambda message: message.author == ctx.author)
                except asyncio.TimeoutError:
                    break
                await msg.delete()
                if msg.content.lower() != "cancel" and msg.content.lower() in ['y', 'n', 'yes', 'no', '0', '1']:
                    options['online'] = (1 if msg.content.lower() in ['y', 'yes', '1'] else 0)
            else:
                break
        await m.clear_reactions()

    @commands.command(aliases=["p"])
    @commands.guild_only()
    async def profile(self, ctx, user: typing.Optional[discord.Member]):
        if not user:
            user = ctx.author
        if await self.globalChecks(ctx, user):
            return
        m = await ctx.send(embed=lembed)
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        player = game["players"][str(user.id)]

        stats = ""
        for k, v in player["skills"].items():
            stats += ''.join([str(self.bot.get_emoji(emojis['starFull'])) for _ in range(v[0])]) + \
                ''.join([str(self.bot.get_emoji(emojis['starEmpty'])) for _ in range(5-v[0])]) + " " + \
                str(self.bot.get_emoji(emojis[k])) + " " + k + " \n"
        xpBar = str(self.bot.get_emoji(emojis["xpStart"])) + (str(self.bot.get_emoji(emojis["xpMiddle"])) * math.ceil((player['xp']/((player['level']*5)+5))*12)) + \
            (str(self.bot.get_emoji(emojis["xpIncomplete"])) * (12-(math.ceil((player['xp']/((player['level']*5)+5))*12)))) + str(self.bot.get_emoji(emojis["xpEnd"]))
        await m.edit(embed=discord.Embed(
            title=f"{self.bot.get_emoji(emojis['RankCard'])} Profile - {user.display_name} | Level {player['level']}",
            description=f"{stats}\n"
                        f"**Experience:** {player['xp']} / {(player['level']*5)+5}\n"
                        f"{xpBar}\n"
                        f"{(str(self.bot.get_emoji(emojis['Warning'])) + ' ') if player['level']-1-player['upgradesUsed'] else ''}"
                        f"**Upgrades avaliable:** {player['level']-1-player['upgradesUsed']}\n\n"
                        f"**Landed on the island:** {humanize.naturaltime(datetime.datetime.utcnow()-datetime.datetime.utcfromtimestamp(player['joined']))}",
            color=colours["b"]
        ))

    @commands.command()
    @commands.guild_only()
    async def map(self, ctx):
        if await self.globalChecks(ctx):
            return
        m = await ctx.send(embed=discord.Embed(
            title="Loading",
            description="This may take some time, please hold",
            color=colours["g"]
        ))
        game = await self.fetchGame(ctx.guild.id, m, ctx)
        if isinstance(game, int):
            return
        w = world.World(online=game['settings']['online'], size=game['settings']['size'], seed=game['settings']['seed'], name=game['settings']['name'], bot=self.bot)
        image = await w.mapimg(ctx=ctx)
        if image == 408:
            return await ctx.reply(embed=discord.Embed(
                title="Oops - That's an error",
                description="We tried generating your map, but it went unresponsive",
                color=colours['r']
            ))

        buf = io.BytesIO()
        image.save(buf, format="png")
        buf.seek(0)
        embed = discord.Embed(title="Game map", color=colours["b"])

        embed.set_image(url="attachment://map.png")
        await m.delete()
        await ctx.reply(embed=embed, file=discord.File(buf, filename="map.png"))
        return buf.close()

    @commands.command()
    @commands.guild_only()
    async def join(self, ctx):
        if await self.globalChecks(ctx):
            return
        await self.addPlayer(ctx, ctx.author)

    @commands.command()
    @commands.guild_only()
    async def dumpgame(self, ctx):
        await ctx.reply(str(await self.fetchGame(ctx.guild.id)))


def setup(bot):
    bot.add_cog(Castaway(bot))
