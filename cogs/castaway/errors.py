from discord.ext import commands


class NoGame(commands.CheckFailure):
    """There is not an active game in the current channel"""

    pass
