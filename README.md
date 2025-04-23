# Tarkov Squad Intel Bot

**A utility-focused Discord bot for Escape from Tarkov squads.**  
This bot provides real-time in-raid support including ammo performance data, item pricing, and planned map intel. Built in Python using `discord.py`, it's designed to serve squads with fast, reliable game information via Discord commands.

---

## Current Features

- `!ping` — Basic connectivity check (bot framework setup)
- `!ammo [caliber]` — Returns ammo options for a given caliber, sorted by penetration power  
  - Accepts user-friendly inputs like `5.45x39`, `9x19`, `7.62x39`
  - Data pulled live from [tarkov.dev](https://tarkov.dev)
- `!calibers` — Lists all supported calibers (based on internal alias mapping)

---

## Project Status

- **Stage**: Core Bot Framework
- **Completed Setup**:
  - Discord bot application and permissions
  - Modular command structure using cogs
  - Working command system with live API integration
- **In Progress**:
  - Error handling and logging
- **Next Planned Features**:
  - `!price [item]` — Real-time flea market pricing
  - `!extracts [map]` — Map-specific extract info
  - `!boss [map]` — Boss spawn chance and behavior lookup

---

## Tech Stack

- Python 3.12+
- `discord.py` (v2+, async)
- `requests` for API calls
- GraphQL integration with [tarkov.dev](https://tarkov.dev/graphql)
- Modular command system using cogs

---

## Setup (Local Dev)

1. Clone the repo
2. Create a `.env` file with your bot token:
   ```env
   DISCORD_TOKEN=your_token_here

---

## Install Dependencies
pip install -r requirements.txt


---

## Run Bot
python bot.py


---