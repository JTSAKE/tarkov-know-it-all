import requests
from discord.ext import commands

TARKOV_API_URL = "https://api.tarkov.dev/graphql"


CALIBER_ALIASES = {
"5.45": "Caliber545x39",
"7.62x39": "Caliber762x39",
"7.62x25": "Caliber762x25TT",
"7.62x51": "Caliber762x51",
"7.62x54": "Caliber762x54R",
"9x18": "Caliber9x18PM",
"9x19": "Caliber9x19Para",
"9x21": "Caliber9x21",
".45": "Caliber1143x23ACP",
".357": "Caliber9x33R",
"9x39": "Caliber9x39",
"12g": "Caliber12g",
"20g": "Caliber20g",
"12.7x55": "Caliber127x55",
"4.6x30": "Caliber46x30",
"5.7x28": "Caliber57x28",
"6.8x51": "Caliber68x51",
"366": "Caliber366TKM",
"300blk": "Caliber762x35",
"23x75": "Caliber23x75",
"338 Lapua": "Caliber86x70",
".50 AE": "Caliber127x33",
"40mmUS": "Caliber40x46",
"40mmRU": "Caliber40mmRU",
}

class Ammo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def calibers(self, ctx):
        """List supported ammo calibers for !ammo command."""
        available = sorted(CALIBER_ALIASES.keys())
        message = "**Supported Calibers:**\n" + ", ".join(f"`{c}`" for c in available)
        
        await ctx.send(message)


    @commands.command()
    async def ammo(self, ctx, caliber: str):
        """Returns a list of ammo for a given caliber, sorted by penetration power."""
        # GraphQL query string with inline fragment
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
        # DEBUG: Show user input and dictionary result
        normalized_input = caliber.strip().lower().replace(" ", "")
        print(f"[DEBUG] User input: {normalized_input}")

        # DEBUG: Try to resolve user input to dictionary result
        api_caliber = CALIBER_ALIASES.get(normalized_input)
        print(f"[DEBUG] Alias lookup result: {api_caliber}")

        # Send the POST request
        response = requests.post(TARKOV_API_URL, json={"query": query})
        if response.status_code != 200:
            await ctx.send("Failed to fetch ammo data.")
            return

        data = response.json().get("data", {}).get("items", [])

        # Normalize the input
        normalized_input = caliber.strip().lower().replace(" ", "")

        # Try to find a mapped caliber
        api_caliber = CALIBER_ALIASES.get(normalized_input)

        # If not in aliases, assume it's a raw Tarkov-style string
        if not api_caliber:
            api_caliber = caliber.strip()  # use as-is

        # Filter by caliber
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

        # Discord message limit = 2000 chars, truncate if needed
        response_message = "\n".join(message_lines)[:1990]
        await ctx.send(response_message)

async def setup(bot):
    await bot.add_cog(Ammo(bot))
