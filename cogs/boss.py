import os
import json
import logging
import time
from discord.ext import commands
from difflib import get_close_matches
from ai.relay import viktor_boss_response

logger = logging.getLogger(__name__)

class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        file_path = os.path.join("data", "bosses.json")
        with open(file_path, "r", encoding="utf-8") as f:
            self.boss_data = json.load(f)

    def find_closest_boss(self, name):
        all_bosses = list(self.boss_data.keys())
        match = get_close_matches(name.title(), all_bosses, n=1, cutoff=0.6)
        return match[0] if match else None
    
    @commands.command()
    async def boss(self, ctx, *, name: str):
        try:
            matched_name = self.find_closest_boss(name)
            if not matched_name:
                await ctx.send(f"No data found for boss '{name}'. Check your spelling or try again.")
                return
            
            boss = self.boss_data[matched_name]
            
            # Start timing GPT response
            start_time = time.perf_counter()

            # Send Viktor’s breakdown
            viktor = await viktor_boss_response(
                boss['name'],
                boss['map'],
                boss['spawn_chance'],
                boss['guard_count'],
                boss['tactics'],
                boss['top_loot']
            )

            latency = time.perf_counter() - start_time
            logger.info("[!BOSS GPT API] Viktor GPT response took %.2f seconds", latency)

            await ctx.send(viktor)

        except Exception as e:
            logger.error(f"[!BOSS] in !boss command: {e}", exc_info=True)
            await ctx.send("Viktor ran into some corrupted intel. Try again later, comrade.")

async def setup(bot):
    await bot.add_cog(Boss(bot))