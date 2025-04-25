from discord.ext import commands
import requests
import difflib
import os
from ai.relay import get_price_commentary

TARKOV_API_URL = "https://api.tarkov.dev/graphql"
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

class Price(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def price(self, ctx, *, item_name: str):
        """Returns flea market price info for an item."""

        query = {
            "query": """
            query {
             items {
                id
                name
                shortName
                avg24hPrice
                lastLowPrice
                sellFor {
                  price
                  source
                }
              }
            }
            """
        }

        response = requests.post(TARKOV_API_URL, json=query)
        if response.status_code != 200:
            await ctx.send("Failed to fetch price data.")
            return

        items = response.json().get("data", {}).get("items", [])

        # Try to find best match
        match = self.find_best_item_match(item_name, items)

        if not match:
            await ctx.send("Couldn’t find a matching item. Try being less bad.")
            return

        #Passing Match to Viktor
        name = match["name"]
        avg_price = match.get("avg24hPrice", 0)
        low_price = match.get("lastLowPrice", 0)

        trader_prices = match.get("sellFor", [])
        trader_summary = "\n".join([f"{t['source']}: {t['price']}₽" for t in trader_prices])

        # Build summary for GPT
        summary = f"""
        Item: {name}
        24h Average Price: {avg_price:,}₽
        Last Known Flea Price: {low_price:,}₽
        Trader Sell Offers:
        {trader_summary}
        """

        # Pass to Viktor
        viktor_response = await get_price_commentary(name, summary)

        await ctx.send(viktor_response)

    def find_best_item_match(self, query, items):
        query = query.strip().lower()
        names = [item["name"].lower() for item in items]
        short_names = [item["shortName"].lower() for item in items if item["shortName"]]

        combined = names + short_names
        best_matches = difflib.get_close_matches(query, combined, n=1, cutoff=0.6)

        if best_matches:
            best = best_matches[0]
            for item in items:
                if item["name"].lower() == best or item["shortName"].lower() == best:
                    return item
        return None


async def setup(bot):
    await bot.add_cog(Price(bot))
