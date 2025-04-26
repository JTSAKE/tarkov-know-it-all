import logging
import os
import requests
import time
from discord.ext import commands
from ai.relay import get_viktor_quest_response
from dotenv import load_dotenv
from difflib import get_close_matches

load_dotenv()

logger = logging.getLogger(__name__)
TARKOV_API_URL = "https://api.tarkov.dev/graphql"
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

class Quest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quest(self, ctx, *, task_name: str):
        """Get quest information by name."""
        try:
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
                logger.error("[!QUEST API] Tarkov.dev API request failed with status %s", response.status_code)
                await ctx.send("Failed to fetch quest data.")
                return

            data = response.json().get("data", {}).get("tasks", [])

            # Fuzzy match the task name
            task_names = [task["name"] for task in data]
            closest_match = get_close_matches(task_name, task_names, n=1, cutoff=0.6)

            if not closest_match:
                logger.warning("[!QUEST MATCHING] No matching quest found for query: %s", task_name)
                await ctx.send(f"No quest found matching '{task_name}'. Try a more exact name.")
                return

            matched_task = next(task for task in data if task["name"] == closest_match[0])

            # Check for special objectives
            has_special_objective = any(
                obj.get("type") in ["findQuestItem", "visit", "extract"]
                for obj in matched_task.get("objectives", [])
            )

            # Time Viktor GPT call
            start_time = time.perf_counter()
            viktor_response = await get_viktor_quest_response(
                matched_task["name"],
                matched_task.get("trader", {}).get("name", "Unknown Trader"),
                matched_task.get("experience", 0),
                matched_task.get("minPlayerLevel", 0),
                matched_task.get("objectives", []),
                has_special_objective
            )

            latency = time.perf_counter() - start_time
            logger.info("[!QUEST GPT API] Viktor GPT response took %.2f seconds", latency)

            await ctx.send(viktor_response)

        except Exception as e:
            logger.exception("[!QUEST] Unexpected error occurred: %s", str(e))
            await ctx.send("Something went wrong pulling that quest info.")

async def setup(bot):
    await bot.add_cog(Quest(bot))
