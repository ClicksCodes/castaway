from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

import config
import datetime
from consts import *

DEV = 0

intents = discord.Intents.default()
intents.members = True

print(f"{C.Cyan}[S] {C.CyanDark}Launching {'dev' if DEV else 'normal'} mode")


class Context(commands.Context):
    async def delete(self):
        if isinstance(self.channel, discord.channel.DMChannel):
            return
        if not self.channel.permissions_for(self.me).manage_messages:
            return
        return await self.message.delete()

    async def reply(self, *args, **kwargs):
        kwargs["mention_author"] = False
        return await self.message.reply(*args, **kwargs)


class Bot(commands.Bot):
    def __init__(self, **kwargs):

        super().__init__(command_prefix=self.get_prefix, help_command=None, **kwargs)

        x = 0
        m = len(config.cogs)
        for cog in config.cogs:
            x += 1
            try:
                print(f"{C.Cyan}[S] {C.CyanDark}Loading cog {x}/{m} ({cog})", end="\r")
                self.load_extension(cog)
                print(f"{C.Green}[S] {C.GreenDark}Loaded cog {x}/{m} ({cog}).")
            except Exception as exc:
                print(f'{C.RedDark}[E] {C.Red}Failed cog {x}/{m} ({cog}) > {exc.__class__.__name__}: {exc}{C.c}')

    async def get_prefix(self, ctx):
        prefixes = ('t[', 't]') if DEV else ('[', ']')
        if not ctx.guild:
            prefixes += ("",)
        return commands.when_mentioned_or(*prefixes)(self, ctx)

    @property
    def prefix(self):
        return "]"

    async def get_context(self, message, *, cls=Context):
        return await super().get_context(message, cls=cls)

    async def on_ready(self):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Castaway island | ]help"), status=discord.Status.online)
        print(f'{C.Pink if DEV else C.Cyan}[S] {C.PinkDark if DEV else C.CyanDark}Logged on as {self.user} [ID: {self.user.id}]{C.c}')


bot = Bot(
    owner_ids=[438733159748599813, 317731855317336067, 261900651230003201, 336532857029656579],
    case_insensitive=True,
    presence=None,
    intents=intents
)

bot.uptime = datetime.datetime.now()
bot.run(config.token)
