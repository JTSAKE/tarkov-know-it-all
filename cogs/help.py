from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")  # Disable default help

    @commands.command()
    async def help(self, ctx):
        message = (
            "**Command Reference:**\n\n"
            "`!ping` — Check if the bot is online.\n"
            "`!ammo [caliber]` — Get a list of ammo for a given caliber.\n"
            "`!calibers` — View all supported caliber inputs.\n"
            "`!help` — Display this help message.\n"
        )
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(CustomHelp(bot))
