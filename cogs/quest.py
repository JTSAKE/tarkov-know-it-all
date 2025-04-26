import discord
from discord.ext import commands
import requests
import os
from ai.relay import get_viktor_quest_response
from dotenv import load_dotenv

load_dotenv()

TARKOV_API_URL = "https://api.tarkov.dev/graphql"
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

class Quest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quest(self, ctx, *, task_name: str):
        """Get quest information by name."""

        query = """
        query {
          tasks {
            id
            name
            trader { name }
            experience
            minPlayerLevel
            objectives {
              description
              type
            }
          }
        }
        """

        response = requests.post(TARKOV_API_URL, json={"query": query})
        if response.status_code != 200:
            await ctx.send("Failed to fetch quest data.")
            return

        data = response.json().get("data", {}).get("tasks", [])
        
        # Fuzzy match the task name
        from difflib import get_close_matches

        task_names = [task["name"] for task in data]
        closest_match = get_close_matches(task_name, task_names, n=1, cutoff=0.6)

        if not closest_match:
            await ctx.send(f"No quest found matching '{task_name}'. Try a more exact name.")
            return

        matched_task = next(task for task in data if task["name"] == closest_match[0])

        # Check for special objectives
        has_special_objective = any(
            obj.get("type") in ["findQuestItem", "visit", "extract"]
            for obj in matched_task.get("objectives", [])
        )

        # Send to Viktor
        viktor_response = await get_viktor_quest_response(
            matched_task["name"],
            matched_task.get("trader", {}).get("name", "Unknown Trader"),
            matched_task.get("experience", 0),
            matched_task.get("minPlayerLevel", 0),
            matched_task.get("objectives", []),
            has_special_objective
        )

        await ctx.send(viktor_response)

async def setup(bot):
    await bot.add_cog(Quest(bot))
