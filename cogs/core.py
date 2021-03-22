import discord
import humanize
import typing
import time
import asyncio
import math
import os
import io
import subprocess
import random
import functools

import datetime
from discord.ext import commands

from consts import *


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.assignees = "PineaFan"

    @commands.command()
    async def stats(self, ctx):
        m = await ctx.send(embed=lembed)
        await m.edit(embed=discord.Embed(
            title="Stats",
            description=f"**Servers:** {len(self.bot.guilds)}\n"
                        f"**Members:** {len(self.bot.users)}\n"
                        f"**Emojis:** {len(self.bot.emojis)}\n"
                        f"**Ping:** {round(self.bot.latency*1000)}ms\n",
            color=colours["b"]
        ))

    @commands.command()
    async def ping(self, ctx):
        m = await ctx.send(embed=lembed)
        time = m.created_at - ctx.message.created_at
        await m.edit(content=None, embed=discord.Embed(title=f"Ping", description=f"Latency is: `{int(time.microseconds / 1000)}ms`", color=colours['b']))

    async def run_sync(self, func: callable, *args, **kwargs):
        return await self.bot.loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

    @commands.command(aliases=["v"])
    async def version(self, ctx):
        head = str(await self.run_sync(subprocess.check_output, ["git", "rev-parse", "HEAD"]))[2:-3]
        branch = str(await self.run_sync(subprocess.check_output, ["git", "rev-parse", "--abbrev-ref", "HEAD"]))[2:-3]
        commit = str(await self.run_sync(subprocess.check_output, ["git", "show-branch", branch]))[(5+(len(branch))):-3]
        url = str(await self.run_sync(subprocess.check_output, ["git", "config", "--get", "remote.origin.url"]))[2:-3]

        total_size = 0
        for path, dirs, files in os.walk("./servers"):
            for f in files:
                fp = os.path.join(path, f)
                total_size += os.path.getsize(fp)

        await ctx.reply(embed=discord.Embed(
            title=f"{self.bot.user.name}",
            description=f"**Repository:** [{url.split('/')[-2]}/{url.split('/')[-1]}]({url})\n"
                        f"**Branch:** `{branch}`\n"
                        f"**HEAD:** `{head}`\n"
                        f"**Commit:** `{commit}`\n"
                        f"**Server size:** `{humanize.naturalsize(os.path.getsize(f'./servers/{ctx.guild.id}.json'))}` • `{humanize.naturalsize(total_size)}`\n"
                        f"**Uptime:** `{str(datetime.datetime.now()-self.bot.uptime).split('.')[0]}`",
            color=colours['b'],
            url="https://discord.gg/bPaNnxe"
        ).set_footer(
            text=f"You probably don't know what most of this means - "
                 f"If you do know what this means, you can become a programmer of {self.bot.user.name} and other bots at https://discord.gg/bPaNnxe",
            icon_url=self.bot.user.avatar_url
        ))

    @commands.command()
    async def bug(self, ctx):
        url = str(await self.run_sync(subprocess.check_output, ["git", "config", "--get", "remote.origin.url"]))[2:-3]
        await ctx.reply(embed=discord.Embed(
            title="Found a bug?",
            description=f"Help us make {self.bot.user.name} better by reporting your issue [here]({url}/issues/new?assignees={self.assignees}&"
                        f"labels=bug&template=bug_report.md&title=%5BBUG%5D), thanks!",
            color=colours["b"]
        ))

    @commands.command()
    async def feature(self, ctx):
        url = str(await self.run_sync(subprocess.check_output, ["git", "config", "--get", "remote.origin.url"]))[2:-3]
        await ctx.reply(embed=discord.Embed(
            title="Want something added or changed?",
            description=f"Help us make {self.bot.user.name} better by giving us your idea [here]({url}/issues/new?assignees={self.assignees}&"
                        f"labels=enhancement&template=feature_request.md&title=%5BADD%5D), thanks!",
            color=colours["b"]
        ))

    @commands.command()
    async def todo(self, ctx):
        url = str(await self.run_sync(subprocess.check_output, ["git", "config", "--get", "remote.origin.url"]))[2:-3]
        await ctx.reply(embed=discord.Embed(
            title="What's on the TODO list?",
            description=f"Help us make {self.bot.user.name} better by giving us your idea [here]({url}/projects/1",
            color=colours["b"]
        ))


def setup(bot):
    bot.add_cog(Core(bot))
