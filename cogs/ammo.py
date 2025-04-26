import logging
import os
import re
import requests
import time
from discord.ext import commands
from ai.relay import get_viktor_response

DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
logger = logging.getLogger(__name__)

TARKOV_API_URL = "https://api.tarkov.dev/graphql"

CALIBER_ALIASES = {
    "545": "Caliber545x39",
    "556": "Caliber556x45NATO",
    "762x39": "Caliber762x39",
    "762x25": "Caliber762x25TT",
    "762x51": "Caliber762x51",
    "762x54": "Caliber762x54R",
    "9x18": "Caliber9x18PM",
    "9x19": "Caliber9x19Para",
    "9x21": "Caliber9x21",
    "45": "Caliber1143x23ACP",
    "357": "Caliber9x33R",
    "9x39": "Caliber9x39",
    "12g": "Caliber12g",
    "20g": "Caliber20g",
    "127x55": "Caliber127x55",
    "46x30": "Caliber46x30",
    "57x28": "Caliber57x28",
    "68x51": "Caliber68x51",
    "366": "Caliber366TKM",
    "300blk": "Caliber762x35",
    "23x75": "Caliber23x75",
    "338lapua": "Caliber86x70",
    "50ae": "Caliber127x33",
    "40mmus": "Caliber40x46",
    "40mmru": "Caliber40mmRU",
}

class Ammo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def calibers(self, ctx):
        """List supported ammo calibers, delivered by Viktor."""
        try:
            available = sorted(CALIBER_ALIASES.keys())
            list_text = "\n".join(f"- {c}" for c in available)

            # Format list into prompt
            prompt = f"""
            You are Viktor 'Relay' Antonov — the sarcastic, post-collapse intel specialist for a PMC team in Tarkov.

            Your commander has asked for a list of supported ammo calibers. You’re not impressed.

            Here’s the list:
            {list_text}

            Respond in-character, with an intro line that sounds annoyed or condescending. Then list the calibers exactly as shown above, using an unordered list format. Feel free to throw in one Russian insult or comment if it fits — with the English meaning in *italics*. No more than 4–6 lines total. Never break character.
            """
            # Time the GPT response for latency monitoring
            start_time = time.perf_counter()

            viktor_response = await get_viktor_response("caliber list", prompt)
            await ctx.send(viktor_response)

            latency = time.perf_counter() - start_time
            logger.info("[!CALIBERS GPT CALL] Viktor GPT response took %.2f seconds", latency)

        except Exception as e:
            logger.exception("[!CALIBERS] Unexpected error: %s", str(e))
            await ctx.send("Viktor refused to list calibers. Probably hungover.")

    @commands.command()
    async def ammo(self, ctx, caliber: str):
        """Returns a list of ammo for a given caliber, sorted by penetration power."""
        try:
            query = """
            query {
                items(type: ammo) {
                    name
                    shortName
                    properties {
                        ... on ItemPropertiesAmmo {
                            caliber
                            damage
                            penetrationPower
                            armorDamage
                            fragmentationChance
                        }
                    }
                }
            }
            """

            # Send the POST request
            response = requests.post(TARKOV_API_URL, json={"query": query})
            if response.status_code != 200:
                logger.error("[!AMMO API] Failed to fetch ammo data. Status code: %s", response.status_code)
                await ctx.send("Failed to fetch ammo data.")
                return

            data = response.json().get("data", {}).get("items", [])

            # Normalize the input
            normalized_input = re.sub(r'[^a-z0-9]', '', caliber.strip().lower())
            api_caliber = CALIBER_ALIASES.get(normalized_input)

            #DEBUG printing user input and alias lookup from caliber dictionary
            if DEBUG_MODE:
                logger.debug("[!AMMO] User input normalized to: %s", normalized_input)
                logger.debug("[!AMMO] Alias lookup result: %s", api_caliber)

            if not api_caliber:
                await ctx.send("Unknown caliber. Try `!calibers` to see what's available.")
                return

            # Filter adn sort caliber
            filtered_ammo = [
                item for item in data
                if item.get("properties")
                and item["properties"].get("caliber", "").strip().lower() == api_caliber.strip().lower()
            ]

            if not filtered_ammo:
                await ctx.send(f"No ammo found for `{caliber}`.")
                return

            # Sort by penetration power (desc)
            sorted_ammo = sorted(filtered_ammo, key=lambda x: x["properties"]["penetrationPower"], reverse=True)

            # Format response
            message_lines = [f"**Top Ammo for `{caliber}` (sorted by pen power):**"]
            for ammo in sorted_ammo:
                p = ammo["properties"]
                message_lines.append(
                    f"**{ammo['name']}** - Pen: {p['penetrationPower']}, Dmg: {p['damage']}, Frag: {int(p['fragmentationChance'] * 100)}%"
                )

            # Format ammo into a readable string for the LLM
            ammo_summary = "\n".join([
                f"{a['name']}: Pen={a['properties'].get('penetrationPower', '?')}, Dmg={a['properties'].get('damage', '?')}"
                for a in sorted_ammo
                if a.get("properties") and a["properties"].get("penetrationPower") is not None
            ])

            # Start timer for GPT latency
            start_time = time.perf_counter()

            # Get GPT response
            viktor_response = await get_viktor_response(caliber, ammo_summary)
            await ctx.send(viktor_response)

            latency = time.perf_counter() - start_time
            logger.info("[!AMMO GPT API] Viktor GPT response took %.2f seconds", latency)

        except Exception as e:
                logger.exception("[!AMMO] Unexpected error: %s", str(e))
                await ctx.send("Something went wrong fetching ammo intel. Viktor is throwing a fit.")

async def setup(bot):
    await bot.add_cog(Ammo(bot))
