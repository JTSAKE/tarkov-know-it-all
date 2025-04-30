import os
import asyncio
import discord
import logging
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
logger = logging.getLogger(__name__)

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

#Signifies the start of a new session
logger.info("--- New Session ---")

#Prints message in terminal to confirm bot is running
@tasks.loop(seconds=60)
async def heartbeat():
    print("[DEBUG] Bot running...")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_command(ctx):
    logger.info(
        "[COMMAND] %s used by %s (%s): %s",
        ctx.command,
        ctx.author.display_name,
        ctx.author.id,
        ctx.message.content
    )

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

async def main():
    await bot.load_extension("cogs.core")
    await bot.load_extension("cogs.ammo")
    await bot.load_extension("cogs.errors")
    await bot.load_extension("cogs.help")
    await bot.load_extension("cogs.price")
    await bot.load_extension("cogs.chat")
    await bot.load_extension("cogs.hideout")
    await bot.load_extension("cogs.boss")
    await bot.load_extension("cogs.quest")
    await bot.start(TOKEN)


@bot.event
async def on_ready():
    print(f"[INFO] Logged in as {bot.user} (ID: {bot.user.id})")
    
    if DEBUG_MODE:
        print("[DEBUG] Debug mode enabled — starting heartbeat")
        heartbeat.start()

asyncio.run(main())
