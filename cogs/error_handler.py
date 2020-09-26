from discord.ext import commands

class Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        def catchall(_, error):
            print(f"Catchall triggered for {error.__class__.__name__}, re-raising")
            raise error

        await getattr(self, error.__class__.__name__, catchall)(ctx, error)

    @staticmethod
    async def CommandNotFound(_ctx, _error):
        pass

    async def GameExists(self, ctx, error):
        await ctx.send("There's already a game going on in this server")

    async def NoFarmsBuilt(self, ctx, error):
        await ctx.send("You don't have a farm built, so you can't run this command")

    async def MaxConcurrencyReached(self, ctx, error):
        if error.per in [commands.BucketType.user, commands.BucketType.member]:
            await ctx.send(f"You're already running this command {str(error.number) + ' time' if error.number != 1 else 'once'}")
        else:
            await ctx.send(f"This command is already being run {str(error.number) + ' time' if error.number != 1 else 'once'} in this {error.per.name}")

    async def NoGame(self, ctx, error):
        await ctx.send("There's not a game in this server")

    async def NoData(self, *args, **kwargs):
        self.NoGame()


def setup(bot):
    bot.add_cog(Handler(bot))