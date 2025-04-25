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
            "`!ammo [caliber]` — Get a list of ammo for a given caliber.\n"
            "`!build [module name]` — View required items, skills, and stations for a hideout module.\n"
            "`!buildlvl [module name]` — Lists available upgrade levels for a hideout module.\n",
            "`!calibers` — View all supported caliber inputs.\n"
            "`!ping` — Check if the bot is online.\n"
            "`!price [item name]` — View item price on flea market and from traders.\n"
            "`!reply [message]` — Chat directly with Viktor and get a personalized response.\n"
            "`!introduce` — Have Viktor introduce himself and share his backstory.\n"
            "`!help` — Display this help message.\n"
        )
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(CustomHelp(bot))
