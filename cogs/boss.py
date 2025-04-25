import discord
from discord.ext import commands
import json
import os
from difflib import get_close_matches
from ai.relay import viktor_boss_response 

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
        matched_name = self.find_closest_boss(name)
        if not matched_name:
            await ctx.send(f"No data found for boss '{name}'. Check your spelling or try again.")
            return
        
        boss = self.boss_data[matched_name]

        # Build a formatted string of the intel
        intel = (
            f"**Name:** {boss['name']}\n"
            f"**Map:** {boss['map']}\n"
            f"**Spawn Chance:** {boss['spawn_chance']}\n"
            f"**Health:** {boss['health']}\n"
            f"**Guards:** {boss['guard_count']}\n"
            f"**Tactics:** {boss['tactics']}\n"
            f"**Top Loot:**\n" + "\n".join(f"- {item}" for item in boss["top_loot"])
        )

        # Send Viktor’s breakdown
        viktor = await viktor_boss_response(
            boss['name'],
            boss['map'],
            boss['spawn_chance'],
            boss['guard_count'],
            boss['tactics'],
            boss['top_loot']
        )
        await ctx.send(viktor)

        # # Send the raw intel block too for clarity
        # await ctx.send(intel[:1990])  # Discord message limit

async def setup(bot):
    await bot.add_cog(Boss(bot))