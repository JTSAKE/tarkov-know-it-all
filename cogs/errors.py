from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument. Use `!help` for usage.")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Unknown command. Use `!help` to see what's available.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument provided. Double-check your input.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send("That command is on cooldown. Try again soon.")
        else:
            await ctx.send("An unexpected error occurred. Please report this to the bot dev.")
            print(f"[ERROR] {type(error).__name__}: {error}")

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
