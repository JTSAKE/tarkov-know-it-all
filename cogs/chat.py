import time
import logging
from discord.ext import commands
from ai.relay import get_viktor_chat 

logger = logging.getLogger(__name__)

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reply(self, ctx, *, message: str):
        """Chat directly with Viktor."""
        try:
            prompt = (
                f"A PMC named {ctx.author.display_name} says: \"{message}\"\n"
                "Respond as Viktor with sarcasm, tactical wisdom, and dark humor. "
                "Include a translated Russian insult in *italics* if needed."
            )
            response = await get_viktor_chat(prompt)

            start_time = time.perf_counter()
            response = await get_viktor_chat(prompt)
            latency = time.perf_counter() - start_time

            logger.info("[!REPLY GPT API] Viktor reply took %.2f seconds", latency)
            await ctx.send(response)
        except Exception as e:
            logger.error("[!REPLY] Error: %s", str(e))
            await ctx.send("Viktor bit his tongue. Try again later.")

    @commands.command()
    async def intro(self, ctx):
        """Have Viktor introduce himself."""
        try:
            prompt = (
                "Introduce yourself as Viktor 'Relay' Antonov — a grizzled, sarcastic ex-PMC who now handles intel for a squad of hopeless operators in Tarkov. "
                "Deliver your background and attitude in under 5 lines. Be gritty and throw in one *Russian swear insult* for flavor."
            )

            start_time = time.perf_counter()
            response = await get_viktor_chat(prompt)
            latency = time.perf_counter() - start_time

            logger.info("[!INTRO GPT API] Viktor intro took %.2f seconds", latency)
            await ctx.send(response)
        except Exception as e:
            logger.error("[!INTRO] Error: %s", str(e))
            await ctx.send("Viktor seems a bit shy today. Try again later.")

async def setup(bot):
    await bot.add_cog(Chat(bot))
