from discord.ext import commands
import requests
import re
from ai.relay import get_viktor_chat
from ai.relay import viktor_hideout_response
from ai.relay import viktor_build_levels_response

TARKOV_API_URL = "https://api.tarkov.dev/graphql"

class Hideout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def build(self, ctx, *, module: str):
        """Look up hideout requirements for a given module (optional: specific level)."""
        # Step 1: Extract level if present
        level_match = re.search(r"(?:level|lvl)?\s*(\d+)$", module.lower())
        requested_level = int(level_match.group(1)) if level_match else None

        # Step 2: Clean module name for fuzzy matching
        cleaned_name = re.sub(r"(?:level|lvl)?\s*\d+$", "", module, flags=re.IGNORECASE).strip().lower()

        # Step 3: Query API
        query = """
        query {
        hideoutStations {
            name
            levels {
            level
            itemRequirements {
                item {
                name
                shortName
                }
                count
            }
            skillRequirements {
                name
                level
            }
            stationLevelRequirements {
                station {
                name
                }
                level
            }
            }
        }
        }
        """
        response = requests.post(TARKOV_API_URL, json={"query": query})
        if response.status_code != 200:
            await ctx.send("Failed to fetch hideout data.")
            return

        stations = response.json().get("data", {}).get("hideoutStations", [])
        selected_station = next(
            (s for s in stations if cleaned_name in s["name"].lower()), None
        )

        if not selected_station:
            await ctx.send(f"Couldn't find a hideout module matching `{module}`.")
            return

        levels_to_show = selected_station["levels"]
        if requested_level:
            levels_to_show = [lvl for lvl in levels_to_show if lvl["level"] == requested_level]
            if not levels_to_show:
                await ctx.send(f"No level {requested_level} found for {selected_station['name']}.")
                return

        lines = [f"**Requirements for {selected_station['name']}**"]

        for level in levels_to_show:
            lines.append(f"\n**Level {level['level']}**")

            items = level.get("itemRequirements", [])
            if items:
                lines.append("**Items:**")
                for item in items:
                    lines.append(f"- {item['item']['name']} x{item['count']}")

            skills = level.get("skillRequirements", [])
            if skills:
                lines.append("**Skills:**")
                for skill in skills:
                    lines.append(f"- {skill['name']} Lv{skill['level']}")

            prereqs = level.get("stationLevelRequirements", [])
            if prereqs:
                lines.append("**Requires:**")
                for req in prereqs:
                    lines.append(f"- {req['station']['name']} Lv{req['level']}")

        # response_message = "\n".join(lines)[:1990]
        # await ctx.send(response_message)

        #Let Viktor interpret the single level requirements
        if requested_level and len(levels_to_show) == 1:
            summary_text = "\n".join(lines)
            viktor = await viktor_hideout_response(selected_station['name'], requested_level, summary_text)
            await ctx.send(viktor)


    @commands.command(name="buildlvl")
    async def build_levels(self, ctx, *, module: str):
        """Show available upgrade levels for a given hideout module."""
        normalized = module.strip().lower()

        query = """
        query {
        hideoutStations {
            name
            levels {
            level
            }
        }
        }
        """
        response = requests.post(TARKOV_API_URL, json={"query": query})
        if response.status_code != 200:
            await ctx.send("Failed to fetch hideout data.")
            return

        stations = response.json().get("data", {}).get("hideoutStations", [])

        selected_station = next(
            (s for s in stations if normalized in s["name"].lower()), None
        )

        if not selected_station:
            await ctx.send(f"Couldn't find a hideout module matching `{module}`.")
            return

        levels = [str(l["level"]) for l in selected_station["levels"]]
        levels_str = ", ".join(f"Lv{lvl}" for lvl in levels)

        # await ctx.send(
        #     f"**{selected_station['name']}** has the following levels: {levels_str}"
        # )

        viktor = await viktor_build_levels_response(selected_station['name'], levels)
        await ctx.send(viktor)

async def setup(bot):
    await bot.add_cog(Hideout(bot))
