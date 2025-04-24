from discord.ext import commands

import logging
logger = logging.getLogger(__name__)

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("🏓 Pong!")

# 👇 This needs to be async in discord.py v2+
async def setup(bot):
    await bot.add_cog(Core(bot))
