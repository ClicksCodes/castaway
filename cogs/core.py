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


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot): self.bot = bot

    @commands.command()
    async def stats(self, ctx):
        m = await ctx.send(embed=loadingEmbed)
        await m.edit(embed=discord.Embed(
            title="Stats",
            description=f"**Servers:** {len(self.bot.guilds)}\n"
                        f"**Members:** {len(self.bot.users)}\n"
                        f"**Emojis:** {len(self.bot.emojis)}\n"
                        f"**Ping:** {round(self.bot.latency*1000)}ms\n",
            color=colours["g"]
        ))

    @commands.command()
    async def ping(self, ctx):
        m = await ctx.send(embed=lembed)
        time = m.created_at - ctx.message.created_at
        await m.edit(content=None, embed=self.createEmbed(f"Ping", f"Latency is: `{int(time.microseconds / 1000)}ms`", colours['g']))


def setup(bot):
    bot.add_cog(Core(bot))
