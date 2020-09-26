from discord.ext import commands
import discord


class Context(commands.Context):
    async def send(self, content=None, **kwargs):
        if kwargs.get("embed", None) is None:
            kwargs["embed"] = discord.Embed(description=content)
            content = None
        return await super().send(content, **kwargs)


class Bot(commands.Bot):
    async def get_context(self, message, *, cls=Context):
        return await super().get_context(message, cls=cls)
