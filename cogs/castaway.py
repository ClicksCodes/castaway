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
            "food": 10,
            "water": 10,
            "skills": {
                "Cooking": [0, 0],
                "Exploring": [0, 0],
                "Crafting": [0, 0],
                "Scavenging": [0, 0],
                "Fishing": [0, 0],
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
                description=f"If you want to restart your island, you can run `{ctx.prefix}end` to start your island over.",
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
                structures = (-2 * options["difficulty"]) + 7
                defaultGame = {
                    "players": {},
                    "tasks": {},
                    "settings": options,
                    "store": {},
                    "storeSize": 1,
                    "resources": {
                        "farms": structures,
                        "mines": structures,
                        "fishing_spots": structures,
                        "undiscovered_land": structures
                    },
                    "started": datetime.datetime.timestamp(datetime.datetime.now()),
                    "structures": {}
                }
                if options["online"]:
                    defaultGame["knownIslands"] = {}
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
                    ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: Text")
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
                    ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: Number")
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
                    ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: Number")
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
                    ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: Number")
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
                    ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: Number")
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
                    ).set_footer(text=f"I'm listening for your next message, {ctx.author.display_name} | Expected: Text")
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
        game = await self.fetchGame(ctx.guild.id)
        if isinstance(game, int):
            return
        player = game["players"][str(ctx.author.id)]
        food = str(self.bot.get_emoji(emojis["food"]["f"])) * (math.floor(player["food"]/2))
        food += str(self.bot.get_emoji(emojis["food"]["h"])) * (player["food"] % 2)
        food += str(self.bot.get_emoji(emojis["food"]["e"])) * (5-math.ceil(player["food"]/2))
        food += f" {player['food']}/10"
        water = str(self.bot.get_emoji(emojis["water"]["f"])) * (math.floor(player["water"]/2))
        water += str(self.bot.get_emoji(emojis["water"]["h"])) * (player["water"] % 2)
        water += str(self.bot.get_emoji(emojis["water"]["e"])) * (5-math.ceil(player["water"]/2))
        water += f" {player['water']}/10"
        hp = str(self.bot.get_emoji(emojis["hp"]["f"])) * (math.floor(player["hp"]/2))
        hp += str(self.bot.get_emoji(emojis["hp"]["h"])) * (player["hp"] % 2)
        hp += str(self.bot.get_emoji(emojis["hp"]["e"])) * (5-math.ceil(player["hp"]/2))
        hp += f" {player['hp']}/10"
        await ctx.reply(embed=discord.Embed(
            title=ctx.author.display_name,
            description=f"{hp}\n"
                        f"{food}\n"
                        f"{water}",
            color=colours["b"]
        ))
        m = await ctx.send(embed=lembed)
        skip = False
        while True:
            if not user:
                user = ctx.author
            if await self.globalChecks(ctx, user):
                return
            game = await self.fetchGame(ctx.guild.id, m, ctx)
            if isinstance(game, int):
                return
            player = game["players"][str(user.id)]

            stats = ""
            for k, v in player["skills"].items():
                stats += ''.join([str(self.bot.get_emoji(emojis['starFull'])) for _ in range(v[0])]) + \
                    ''.join([str(self.bot.get_emoji(emojis['starEmpty'])) for _ in range(5-v[0])]) + " " + \
                    str(self.bot.get_emoji(emojis[k])) + " " + k + " \n"
            xpBar = str(self.bot.get_emoji(emojis["xpStart"])) + \
                (str(self.bot.get_emoji(emojis["xpMiddle"])) * math.ceil((player['xp']/((player['level']*10*game["settings"]["difficulty"])+10))*12)) + \
                (str(self.bot.get_emoji(emojis["xpIncomplete"])) *
                    (12-(math.ceil((player['xp']/((player['level']*(10*game["settings"]["difficulty"]))+10))*12)))) + str(self.bot.get_emoji(emojis["xpEnd"]))
            upgradesAvaliable = player['level']-1-player['upgradesUsed']
            await m.edit(embed=discord.Embed(
                title=f"{self.bot.get_emoji(emojis['RankCard'])} Profile - {user.display_name} | Level {player['level']}",
                description=f"{stats}\n"
                            f"**Experience:** {player['xp']} / {(player['level']*10*game['settings']['difficulty'])+10}\n"
                            f"{xpBar}\n"
                            f"{(str(self.bot.get_emoji(emojis['Warning'])) + ' ') if upgradesAvaliable else ''}"
                            f"**Upgrades avaliable:** {player['level']-1-player['upgradesUsed']}\n\n"
                            f"**Landed on the island:** {humanize.naturaltime(datetime.datetime.utcnow()-datetime.datetime.utcfromtimestamp(player['joined']))}",
                color=colours["b"]
            ))
            if upgradesAvaliable and ctx.author == user:
                if not skip:
                    await m.add_reaction(self.bot.get_emoji(emojis['Warning']))
                    try:
                        reaction = await ctx.bot.wait_for('reaction_add', timeout=60, check=lambda r, user: r.message.id == m.id and user == ctx.author)
                    except asyncio.TimeoutError:
                        await m.clear_reactions()
                        break

                    try:
                        r = reaction[0].emoji
                    except AttributeError:
                        await m.clear_reactions()
                        break

                    try:
                        await m.clear_reactions()
                        await asyncio.sleep(0.1)
                    except Exception as e:
                        break
                        print(e)

                if r.name.lower() == "warning" or skip:
                    if not skip:
                        for r in [emojis["Cooking"], emojis["Exploring"], emojis["Crafting"], emojis["Scavenging"], emojis["Fishing"], emojis["Mining"], emojis["Farming"]]:
                            await m.add_reaction(self.bot.get_emoji(r))
                    try:
                        reaction = await ctx.bot.wait_for('reaction_add', timeout=60, check=lambda r, user: r.message.id == m.id and user == ctx.author)
                    except asyncio.TimeoutError:
                        await m.clear_reactions()
                        break

                    try:
                        r = reaction[0].emoji
                    except AttributeError:
                        await m.clear_reactions()
                        break

                    skip = False
                    try:
                        game = await self.fetchGame(ctx.guild.id, m, ctx)
                        game["players"][str(ctx.author.id)]["skills"][r.name][0] += 1
                        game["players"][str(ctx.author.id)]["upgradesUsed"] += 1
                        await self.writeGame(ctx.guild.id, game, ctx, m)
                        if game["players"][str(ctx.author.id)]['level']-1-game["players"][str(ctx.author.id)]['upgradesUsed'] > 0:
                            skip = True
                            await m.remove_reaction(r, ctx.author)
                        else:
                            await m.clear_reactions()
                    except KeyError:
                        pass

                    try:
                        if not skip:
                            await m.clear_reactions()
                            await asyncio.sleep(0.1)
                    except Exception as e:
                        print(e)
                        break
            else:
                break
        await m.clear_reactions()

    @commands.command(aliases=["map", "is"])
    @commands.guild_only()
    async def island(self, ctx):
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
        embed = discord.Embed(
            title=f"{game['settings']['name']} ({len(game['players'])} islanders)",
            description=f"**Community storage size:** {(game['storeSize']**2)*100} items ({sum([v for k, v in game['store'].items()])} used)\n"
                        f"**Players currently working:** {len(game['tasks'])}\n"
                        f"**Resource piles:** {sum([v for k, v in game['resources'].items()])}\n"
                        f"**Map size:** {game['settings']['size'][0]}x{game['settings']['size'][1]}\n"
                        f"**Map seed:** {game['settings']['seed']}\n"
                        f"**Island created:** {datetime.datetime.fromtimestamp(game['started']).strftime('20%y-%m-%d')} "
                        f"({humanize.naturaldelta(datetime.datetime.now()-datetime.datetime.fromtimestamp(game['started']))} ago)\n",
            color=colours["b"]
        )

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
    async def end(self, ctx):
        if await self.globalChecks(ctx):
            return
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.reply(embed=discord.Embed(
                title="You can't do that >:(",
                description="You need to have the `manage_server` permission to end a game",
                color=colours["r"]
            ))
        m = await ctx.reply(embed=discord.Embed(
            title="You sure?",
            description=f"This will completely delete your island from the face of the earth - it cannot be recovered.\n"
                        f"You can {self.bot.get_emoji(emojis['tick'])} confirm deletion or {self.bot.get_emoji(emojis['cross'])} delete your island",
            color=colours["o"]
        ).set_footer(text=f"I'm listening for your next reaction, {ctx.author.display_name} | Expected: Reaction"))

        for r in [emojis['tick'], emojis['cross']]:
            await m.add_reaction(self.bot.get_emoji(r))

        try:
            reaction = await ctx.bot.wait_for('reaction_add', timeout=60, check=lambda r, user: r.message.id == m.id and user == ctx.author)
        except asyncio.TimeoutError:
            return

        try:
            r = reaction[0].emoji
        except AttributeError:
            return

        try:
            await m.remove_reaction(r, ctx.author)
        except Exception as e:
            print(e)

        if r.name == "tick":
            await m.delete()
            os.remove(f"servers/{ctx.guild.id}.json")
            await ctx.reply(embed=discord.Embed(
                title="Poof",
                description=f"Thats it, your game cannot be recovered. If you want to start again, just `{ctx.prefix}start`",
                color=colours["o"]
            ))
        else:
            await m.delete()

    @commands.command()
    @commands.guild_only()
    async def leave(self, ctx):
        if await self.globalChecks(ctx, ctx.author):
            return
        m = await ctx.reply(embed=discord.Embed(
            title="You sure?",
            description=f"You will be removed from the island, along with your items.\n"
                        f"You can {self.bot.get_emoji(emojis['tick'])} confirm deletion or {self.bot.get_emoji(emojis['cross'])} delete your island",
            color=colours["o"]
        ).set_footer(text=f"I'm listening for your next reaction, {ctx.author.display_name} | Expected: Reaction"))

        for r in [emojis['tick'], emojis['cross']]:
            await m.add_reaction(self.bot.get_emoji(r))

        try:
            reaction = await ctx.bot.wait_for('reaction_add', timeout=60, check=lambda r, user: r.message.id == m.id and user == ctx.author)
        except asyncio.TimeoutError:
            return

        try:
            r = reaction[0].emoji
        except AttributeError:
            return

        try:
            await m.remove_reaction(r, ctx.author)
        except Exception as e:
            print(e)

        if r.name == "tick":
            game = await self.fetchGame(ctx.guild.id, m, ctx)
            if isinstance(game, int):
                return
            del game["players"][str(ctx.author.id)]
            await self.writeGame(ctx.guild.id, game, ctx, m)
            await m.delete()
            await ctx.reply(embed=discord.Embed(
                title="Poof",
                description=f"Thats it, you've left. If you want to join again, just `{ctx.prefix}join`",
                color=colours["o"]
            ))
        else:
            await m.delete()

    @commands.command(aliases=["m"])
    @commands.guild_only()
    async def manual(self, ctx):
        if await self.globalChecks(ctx, ctx.author):
            return
        c = ctx.prefix
        keys = {
            0: [
                "Islands",
                "An island is where each game of Castaway takes place - It has a name, map, and some islanders trying to escape\n\n"
                f"{self.bot.get_emoji(emojis['Name'])} **Name:** The island name is just how you recognise it against others\n"
                f"{self.bot.get_emoji(emojis['Max_Players'])} **Max players:** The amount of people allowed on the island, any others won't be able to join\n"
                f"{self.bot.get_emoji(emojis['Size'])} **Size:** The size of your island decides how many resources can be found\n"
                f"{self.bot.get_emoji(emojis['Seed'])} **Seed:** Seeds are used to generate your map, not too important\n"
                f"{self.bot.get_emoji(emojis['Difficulty'][2])} **Difficulty:** Affects item drop rates, and how long you have to work for the same reward\n"
                f"{self.bot.get_emoji(emojis['Online'][1])} **Online:** Lets your interact with other servers, and other servers interact with your island\n"
            ],
            1: [
                "Players",
                "Each player has a list of statistics and information about them\n\n"
                f"{self.bot.get_emoji(emojis['food']['f'])} **Food:** Food is increased with `{c}eat` and is needed to stop losing health when working\n"
                f"{self.bot.get_emoji(emojis['water']['f'])} **Water:** Food is increased with `{c}drink` and is also needed to stop losing health when working\n"
                f"Both Food and Water will decrease the amount of items gained when working - so make sure to keep them high\n"
                f"{self.bot.get_emoji(emojis['hp']['f'])} **HP:** Your health decreases if you are on low food and water, "
                f"and losing your health clears your items and halves your stats\n"
                f"{self.bot.get_emoji(emojis['starFull'])} **Skills:** Skills help you complete tasks faster and more efficiently. Someone good at scavenging can "
                f"gain more items than someone at level 1\n"
                f"{self.bot.get_emoji(emojis['Warning'])} **XP and upgrades:** As you complete activities, your player skill level increases. Each time you level up,"
                f" you can upgrade any skill."
            ],
            2: [
                "Working",
                "Working is how you get items on your island. It is affected by skills and difficulty\n\n"
                f"{self.bot.get_emoji(emojis['Cooking'])} **Cooking:** `{c}cook` Converts raw food to cooked variants, with better nutrition\n"
                f"{self.bot.get_emoji(emojis['Exploring'])} **Exploring:** `{c}explore` Looks for new places on the map for activities which require them\n"
                f"{self.bot.get_emoji(emojis['Crafting'])} **Crafting:** `{c}craft` or `{c}c` *See Crafting*\n"
                f"{self.bot.get_emoji(emojis['Scavenging'])} **Scavenging:** `{c}scavenge` or `{c}collect` Uses `Undiscovered land`, and collects small items like wood\n"
                f"{self.bot.get_emoji(emojis['Fishing'])} **Fishing:** `{c}fish` uses `Fishing spots`, and collects fish from the water to be cooked and eaten\n"
                f"{self.bot.get_emoji(emojis['Mining'])} **Mining:** `{c}mine` uses `Mines`, and collects metals and ores for crafting\n"
                f"{self.bot.get_emoji(emojis['Farming'])} **Farming:** `{c}farm` uses `Farms`, and collects various food items, some of which need to be cooked\n"
            ],
            3: [
                "Crafting",
                "Crafting lets you convert resources into materials and structures. Crafting takes time and can be sped up with the crafting skill\n\n"
                "**IDs:** Each item has an ID, which is shown as a `number` before items. These are used for deciding what to craft\n"
                "**Skill:** Crafting does not increase naturally, and can only increase when you gain a player level from other activities\n"
                f"**Items:** A list of items and how to craft them can be seen on `{c}craft` or `{c}c`. For more information on an item, you can `{c}item` followed by its ID\n"
            ],
            4: [
                "Inventory",
                "Your inventory is where items are stored for yourself personally. These can be transferred\n\n"
                f"There is an infinite capacity for your inventory, but only you can access; it using `{c}inventory`, `{c}inv` or `{c}i`.\n"
                f"{self.bot.get_emoji(emojis['Transfer'])} Any item can be transferred from your inventory to the server storage, and the other way around\n"
                f"{self.bot.get_emoji(emojis['Delete'])} Delete any unused items, losing them forever\n"
                f"{self.bot.get_emoji(emojis['Sort'])} All items in your inventory can be sorted easily, in order of their ID\n"
            ],
            5: [
                "Store",
                "The community store is where items are stored for everyone to take. These can be transferred\n\n"
                f"There is a limited capacity for your the store, and it can be accessed using `{c}store` or `{c}s`.\n"
                f"This capacity can be increased using `{c}craft 50` or `{c}c 50`.\n"
                f"{self.bot.get_emoji(emojis['Transfer'])} Any item can be transferred from the store to your inventory, and the other way around\n"
                f"{self.bot.get_emoji(emojis['Sort'])} All items in the server can be sorted easily, in order of their ID\n"
            ]
        }
        page = 0
        m = await ctx.send(embed=lembed)
        for r in [emojis["left"], emojis["cross"], emojis["right"]]:
            await m.add_reaction(self.bot.get_emoji(r))
        while True:
            await m.edit(embed=discord.Embed(
                title=f"Manual: {keys[page][0]} ({page+1}/{len(keys.keys())})",
                description=keys[page][1],
                color=colours['b']
            ).set_footer(text=f"I'm listening for your next reaction, {ctx.author.display_name} | Expected: Reaction"))
            try:
                done, _ = await asyncio.wait([
                    ctx.bot.wait_for('reaction_add', timeout=120, check=lambda _, user: user == ctx.author),
                    ctx.bot.wait_for('reaction_remove', timeout=120, check=lambda _, user: user == ctx.author)
                ], return_when=asyncio.FIRST_COMPLETED)
            except asyncio.TimeoutError:
                break

            try:
                response = done.pop().result()
                await m.remove_reaction(response[0].emoji, ctx.author)
                if response[0].emoji.name == "cross":
                    break
                elif response[0].emoji.name == "left":
                    page -= 1
                else:
                    page += 1
                page = min(max(0, page), len(keys.keys())-1)
            except Exception as e:
                print(e)
            for future in done:
                future.exception()
        await asyncio.sleep(0.8)
        await m.clear_reactions()

    @commands.command()
    @commands.guild_only()
    async def dumpgame(self, ctx):
        await ctx.reply(str(await self.fetchGame(ctx.guild.id)))


def setup(bot):
    bot.add_cog(Castaway(bot))
