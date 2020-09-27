from discord.ext import commands


class NoGame(commands.CheckFailure):
    """There is not an active game in the current guild"""  # ERRORS everywhere!

    pass


class NoData(NoGame):
    """There is not an active game in the current guild, and in fact there's no data on the current guild at all"""

    pass  # Ill continue writing comments tomorrow.


class GameExists(commands.CheckFailure):
    """There is already an active game in the current guild"""

    pass  # No you won't -3665


class NoFarmsBuilt(commands.CheckFailure):
    """No farm is in the server"""

    pass
