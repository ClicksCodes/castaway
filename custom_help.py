from discord.ext import commands


class Help(commands.DefaultHelpCommand):
    def __init__(self, *args, **kwargs):
        kwargs["paginator"] = kwargs.get("paginator", commands.Paginator(prefix="```diff\n"))
        super().__init__(*args, **kwargs)

