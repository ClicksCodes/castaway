from discord.ext import commands


class NoGame(commands.CheckFailure):
    """There is not an active game in the current guild"""  # ERRORS everywhere!
    pass

class NoData(NoGame):
    """There is not an active game in the current guild, and in fact there's no data on the current guild at all"""
    pass  # Ill continue writing comments tomorrow.