from discord.ext import commands
from ai.relay import get_viktor_chat 

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reply(self, ctx, *, message: str):
        """Chat directly with Viktor."""
        prompt = (
            f"A PMC named {ctx.author.display_name} says: \"{message}\"\n"
            "Respond as Viktor with sarcasm, tactical wisdom, and dark humor. "
            "Include a translated Russian insult in *italics* if needed."
        )
        response = await get_viktor_chat(prompt)
        await ctx.send(response)

    @commands.command()
    async def introduce(self, ctx):
        """Have Viktor introduce himself."""
        prompt = (
            "Introduce yourself as Viktor 'Relay' Antonov — a grizzled, sarcastic ex-PMC who now handles intel for a squad of hopeless operators in Tarkov. "
            "Deliver your background and attitude in under 5 lines. Be gritty and throw in one *Russian swear insult* for flavor."
        )
        response = await get_viktor_chat(prompt)
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(Chat(bot))
