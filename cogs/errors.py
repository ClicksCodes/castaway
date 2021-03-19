import copy
import discord
import json
import humanize
import aiohttp
import traceback
import typing
import time
import asyncio
import postbin
import os

from datetime import datetime
from discord.ext import commands
from textwrap import shorten
from hashlib import sha256
from consts import *


class Errors(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            # Normal Green
            # Warning Yellow
            # Critical Red
            # Status Blue
            try:
                code = str(sha256(str.encode(str(ctx.message.id))).hexdigest())[50:]
            except Exception as e:
                print(e)
                code = ctx.message.id

            if isinstance(error, commands.errors.NoPrivateMessage):
                return print(f"{C.GreenDark}[N] {C.Green}{str(error)}{C.c}")
            elif isinstance(error, commands.errors.BotMissingPermissions):
                return print(f"{C.GreenDark}[N] {C.Green}{str(error)}{C.c}")
            elif isinstance(error, commands.errors.CommandNotFound):
                return print(f"{C.GreenDark}[N] {C.Green}{str(error)}{C.c}")
            elif isinstance(error, asyncio.TimeoutError):
                return print(f"{C.GreenDark}[N] {C.Green}{str(error)}{C.c}")
            elif isinstance(error, commands.errors.NotOwner):
                return print(f"{C.GreenDark}[N] {C.Green}{str(error)}{C.c}")
            elif isinstance(error, commands.errors.TooManyArguments):
                return print(f"{C.GreenDark}[N] {C.Green}{str(error)}{C.c}")
            elif isinstance(error, commands.errors.MissingPermissions):
                return await ctx.send(embed=discord.Embed(
                    title=f"{self.bot.get_emoji(emojis['cross'])} Missing permissions",
                    description=str(error),
                    color=colours["r"]
                ))
            else:
                tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
                if "clear_reactions()" in tb:
                    return
                string = f"Command ran: {ctx.message.content}\nUser id:{ctx.author.id}\nGuild id:{ctx.guild.id}\n\n{tb}"
                tb = "```" + ("\n".join([f"[C]" + line for line in (string.split("\n"))])) + "```"
                # url = await postbin.postAsync(tb)
                print(f"{C.RedDark}[C] {C.Red}FATAL:\n{tb}{C.c}\n{code}")
                if self.bot.user.id == 757225562816118895:
                    # await self.bot.get_channel(791592620551307264).send(embed=discord.Embed(
                    #     title="Error",
                    #     description=f"`{code}`: " + url,
                    #     color=colours["r"]
                    # ))
                    # return await ctx.channel.send(embed=discord.Embed(
                    #     title="It looks like I messed up",
                    #     description=f"It looks like there was an error. Just send the [developers](https://discord.gg/bPaNnxe) code `{code}`",
                    #     color=colours["r"]
                    # ))
                    return await ctx.send(embed=discord.Embed(
                        title="Error",
                        description=str("```" + "".join(traceback.format_exception(type(error), error, error.__traceback__)).split("\n")[-2] + "```"),
                        color=colours["r"]
                    ))
                else:
                    return
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_error(event, *args, **kwargs):
        tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        tb = f"Command ran: {ctx.message.content}\nUser id:{ctx.author.id}\nGuild id:{ctx.guild.id}\n\n{tb}"
        return print(f"{C.RedDark}[C] {C.Red}Error Below\n{tb}{C.c}")

    @commands.command()
    @commands.is_owner()
    async def error(self, ctx):
        raise Warning("Error has no attribute Error")


def setup(bot):
    bot.add_cog(Errors(bot))
