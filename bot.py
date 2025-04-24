import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import asyncio
from discord.ext import tasks

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

#Setup structured logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),  # Logs to terminal
        logging.FileHandler("bot.log", encoding="utf-8")  # Logs to file
    ]
)

#Enable Heartbeat when env setting set to true.
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}!")

async def main():
    await bot.load_extension("cogs.core")
    await bot.load_extension("cogs.ammo")
    await bot.load_extension("cogs.errors")
    await bot.load_extension("cogs.help")
    await bot.start(TOKEN)

@bot.event
async def on_ready():
    print(f"[INFO] Logged in as {bot.user} (ID: {bot.user.id})")
    
    if DEBUG_MODE:
        print("[DEBUG] Debug mode enabled — starting heartbeat.")
        heartbeat.start()

@tasks.loop(seconds=60)
async def heartbeat():
    print("[DEBUG] Bot running...")

asyncio.run(main())
