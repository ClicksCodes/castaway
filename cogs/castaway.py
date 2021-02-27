import discord
import humanize
import typing
import time
import asyncio
import math
import io
import random

from datetime import datetime
from discord.ext import commands

from consts import *
from . import types
from . import world


class Castaway(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def globalChecks(self, ctx, user=None):
        if ctx.guild.id not in self.bot.games:
            await ctx.send(embed=discord.Embed(
                    title=f"{emojis['Warning']} Your server doesn't have an island",
                    description=f"You'll need to run `{ctx.prefix}start` to start up your island.",
                    color=colours["r"]
                ))
            return True
        if user:
            if user.id not in self.bot.games[ctx.guild.id]["players"]:
                await ctx.send(embed=discord.Embed(
                    title=f"{emojis['RankCard']} {user.display_name} hasn't joined the yet",
                    description=f"{user.display_name} isn't on the island yet. Get them to run `{ctx.prefix}join` to enter the island.",
                    color=colours["r"]
                ))
                return True
        return False

    @commands.command()
    @commands.guild_only()
    async def start(self, ctx):
        if ctx.guild.id in self.bot.games:
            return await ctx.send(embed=discord.Embed(
                title=f"{emojis['Warning']} Your server has already started",
                description=f"If you want to restart your island, you can run `{ctx.prefix}restart` to start your island over.",
                color=colours["r"]
            ))
        options = {
            "name": "Castaway Island",
            "max_players": 0,
            "size": (25, 25),
            "seed": random.randint(0, 100000000),
            "difficulty": 2,
            "online": False
        }
        m = await ctx.send(embed=lembed)
        for _ in range(0, 50):
            diffstring = 'Easy' if options['difficulty'] == 1 else 'Normal' if options['difficulty'] == 2 else 'Hard'
            await m.edit(embed=discord.Embed(
                title="Island setup",
                description=f"{emojis['Name']                              } **Name:** {options['name']}\n"
                            f"{emojis['Max_Players']                       } **Max Players:** {options['max_players']}\n"
                            f"{emojis['Size']                              } **Size:** {options['size'][0]}x{options['size'][1]}\n"
                            f"{emojis['Seed']                              } **Seed:** `{options['seed']}`\n"
                            f"{emojis['Difficulty'][options['difficulty']] } **Difficulty:** {diffstring}\n"
                            f"{emojis['Online'][int(options['online'])]    } **Online:** {'Yes' if options['online'] else 'No'}",
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
                    )
                )
                w = world.World(online=options["online"], seed=options["seed"], size=options["size"])
                self.bot.games[ctx.guild.id] = {"players": {}, "world": w, "tasks": {}, "settings": options}

                return

            elif r.name == "cross":
                break
            elif r.name == "Name":
                await m.clear_reactions()
                await m.edit(embed=discord.Embed(
                        title=f"{emojis['Name']} What should the island be called?",
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
                await m.edit(embed=discord.Embed(
                        title=f"{emojis['Max_Players']} How many people should be allowed on the island?",
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
                await m.edit(embed=discord.Embed(
                        title=f"{emojis['Size']} How big should your island be?",
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
                await m.edit(embed=discord.Embed(
                        title=f"{emojis['Seed']} What should your island seed be?",
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
                await m.edit(embed=discord.Embed(
                        title=f"{emojis['Difficulty'][2]} What should your game difficulty be?",
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
                await m.edit(embed=discord.Embed(
                        title=f"{emojis['Name']} Want to play online?",
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

    @commands.command()
    @commands.guild_only()
    async def profile(self, ctx, user: typing.Optional[discord.Member]):
        if not user:
            user = ctx.author
        if await self.globalChecks(ctx, user):
            return
        player = self.bot.games[ctx.guild.id]["players"][user.id]

        stats = ""
        for k, v in player.skills.items():
            stats += ''.join([emojis['starFull'] for _ in range(v[0])]) +
            ''.join([emojis['starEmpty'] for _ in range(5-v[0])]) + " " + self.bot.games[ctx.guild.id]["players"][ctx.author.id].skills[k][1] + " " + k + " \n"
        xpBar = emojis["xpStart"] + (emojis["xpMiddle"] * math.ceil((player.xp/((player.level*5)+5))*12)) + \
            (emojis["xpIncomplete"] * (12-(math.ceil((player.xp/((player.level*5)+5))*12)))) + emojis["xpEnd"]
        await ctx.reply(embed=discord.Embed(
            title=f"{emojis['RankCard']} Profile - {user.display_name} | Level {player.level}",
            description=f"{stats}\n"
                        f"**Experience:** {player.xp} / {(player.level*5)+5}\n"
                        f"{xpBar}\n"
                        f"{(emojis['Warning'] + ' ') if player.level-1-player.upgradesUsed else ''}**Upgrades avaliable:** {player.level-1-player.upgradesUsed}\n\n"
                        f"**Landed on the island:** {humanize.naturaltime(datetime.utcnow()-player.joined)}",
            color=colours["b"]
        ))

    @commands.command()
    @commands.guild_only()
    async def map(self, ctx):
        if await self.globalChecks(ctx):
            return
        image = self.bot.games[ctx.guild.id]["world"].mapimg(ctx=ctx, bot=self.bot)

        buf = io.BytesIO()
        image.save(buf, format="png")
        buf.seek(0)
        embed = discord.Embed(title="Game map", color=colours["b"])

        embed.set_image(url="attachment://map.png")
        return await ctx.reply(embed=embed, file=discord.File(buf, filename="map.png"))
        buf.close()

    @commands.command()
    async def debug(self, ctx):
        await ctx.reply(self.bot.games)
        # await ctx.delete()


def setup(bot):
    bot.add_cog(Castaway(bot))
