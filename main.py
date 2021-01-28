DEV = 0
import discord
from discord.ext import commands

import sys
import traceback
import config
import json

from consts import *

intents = discord.Intents.default()
intents.members = True

print(f"{c.Cyan}[S] {c.CyanDark}Launching {'dev' if DEV else 'normal'} mode")


class Context(commands.Context):
    async def delete(self):
        if isinstance(self.channel, discord.channel.DMChannel): return
        if not self.channel.permissions_for(self.me).manage_messages: return
        await self.message.delete()
    
    async def reply(self, *args, **kwargs):
        kwargs["mention_author"] = False
        await self.message.reply(*args, **kwargs)


class Bot(commands.Bot):
    def __init__(self, **kwargs):

        super().__init__(command_prefix=self.get_prefix, help_command=None, **kwargs)

        x = 0
        m = len(config.cogs)
        for cog in config.cogs:
            x += 1
            try:
                print(f"{c.Cyan}[S] {c.CyanDark}Loading cog {x}/{m} ({cog})", end="\r")
                self.load_extension(cog)
                print(f"{c.Green}[S] {c.GreenDark}Loaded cog {x}/{m} ({cog}).")
            except Exception as exc:
                print(f'{c.RedDark}[E] {c.Red}Failed cog {x}/{m} ({cog}) > {exc.__class__.__name__}: {exc}{c.c}')
    
    async def get_prefix(self, ctx):
        prefixes = ('t[', 't]' if DEV else '[', ']')
        if not ctx.guild: prefixes += ("",)
        return commands.when_mentioned_or(*prefixes)(self, ctx)

    @property
    def prefix(self):
        try:
            return self.get_prefix(ctx)[2]
        except Exception as e:
            return "@Castaway "  # This should **never** trigger
    
    async def get_context(self, message, *, cls=Context):
        return await super().get_context(message, cls=cls)

    async def on_ready(self):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Castaway island | ]help"), status=discord.Status.online)
        print(f'{c.Pink if DEV else c.Cyan}[S] {c.PinkDark if DEV else c.CyanDark}Logged on as {self.user} [ID: {self.user.id}]{c.c}')

bot = Bot(
    owner_ids=[438733159748599813, 317731855317336067, 261900651230003201, 336532857029656579], 
    case_insensitive=True, 
    presence=None,
    intents=intents
)
bot.games = {}
bot.run(config.token if not DEV else config.dtoken)
