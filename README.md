# Tarkov Know-It-All Bot — "Viktor 'Relay' Antonov"

A Discord bot built for Escape From Tarkov players. Viktor is more than a bot — he's your squad's embedded PMC intel specialist. Tactical, sarcastic, and occasionally offensive (in Russian, with translations). This project combines real-time game data with OpenAI to deliver immersive, role-play-driven squad support.

---

## Current Features

### Core Framework
- Modular command system using Discord.py cogs
- Structured error handling and logging (`logs/bot.log`)
- Custom in-character `!help` command
- GPT-powered character layer with OpenAI API integration
- Fuzzy matching for user input (boss names, calibers, items)
- Dev mode tools (heartbeat loop, debug logging toggle)
- `.env` support for secure API key and mode management
- Static data handling via JSON files (`data/bosses.json`)

---

### `!ammo <caliber>`
Fetches real-time ammo data from the [Tarkov.dev](https://tarkov.dev) API and sends it through OpenAI's GPT model.

- Returns top-performing ammo by penetration
- Supports fuzzy aliases (e.g., `!ammo 9x19`)
- Viktor gives a tactical, sarcastic ammo briefing
- GPT-driven personality in full effect

---

### `!calibers`
- Returns a list of supported ammo calibers
- Response is in-character from Viktor
- Delivered with attitude and a jab or two for even asking

---

### `!price <item name>`
Fetches flea market and trader prices from the [Tarkov.dev](https://tarkov.dev) API and sends it through OpenAI's GPT model.

- Uses fuzzy matching (`gpu` → `Graphics Card`)
- Live pricing from Tarkov.dev (24h average, low, trader offers)
- GPT formats the data into a short, snarky market analysis
- Viktor tells you if it's “worth dying for” or “trader trash”

---

###  `!boss <boss name>`
Intel report on any boss in Tarkov, delivered by Viktor.
- Fuzzy name matching (`tagilla`, `killa`, `shadow`, etc.)
- Includes spawn location, spawn chance, guards, tactics, and loot
- Viktor summarizes with a snarky personality via GPT
- Great for pre-raid planning or squad banter

---

###  `!build <module name>`
Fetches build requiredments from the [Tarkov.dev](https://tarkov.dev) API and sends it through OpenAI's GPT model.
- Returns all requirements to build or upgrade a hideout module.
- Fuzzy-matches hideout station names (bitcoin, medstation, water, etc.)
- Shows item counts, skill levels, and prerequisite modules for each level
- Pulls real-time data from Tarkov.dev's hideout structure
- Future-ready for Viktor to critique your base-building priorities

---

### `!buildlvl <module name>`
Fetches build levels from the [Tarkov.dev](https://tarkov.dev) API and sends it through OpenAI's GPT model.
- Lists all upgrade levels available for a given hideout module.
- Fuzzy-matches hideout station names (lavatory, intel, med, etc.)
- Displays available levels in a clean list (e.g., Lv1, Lv2, Lv3)
- Useful for planning what’s possible before gathering materials
- Viktor adds commentary about your ambitions (or lack thereof)

---

### `!intro`
Have Viktor explain who (and what) he is.
- Viktor gives his gritty, sarcastic backstory
- Responds with tactical wisdom and Russian-flavored insults
- Sets the tone for how he interacts with the squad
- Perfect intro for new team members

---

### `!quest <quest name>`
Fetches quest details from the [Tarkov.dev](https://tarkov.dev) API and sends it through OpenAI's GPT model.
- Live quest data pulled from Tarkov.dev
- Shows quest name, trader, XP reward, and objectives
- Viktor summarizes with sarcasm, insults, and tactical advice
- Automatically links to the Tarkov Wiki for complex quests

---

### `!reply <message>`
Chat directly with Vikor in real-timee.
- GPT-powered banter with Viktor’s sarcastic tone
- Responds with tactical wisdom and Russian-flavored insults
- Great for roleplay, squad immersion, or laughs
- Every message generates a unique, in-character reply

---

## Viktor: The Personality

Viktor "Relay" Antonov is a grizzled, ex-military AI advisor.

- Built using OpenAI’s `gpt-4.1-nano`
- Responses shaped by system and user prompt engineering
- Drops occasional Russian insults (with *English translations*)
- Never breaks character. Ever.

---

## Planned Features

- Player Lookup Command - Look up player stats and profiles and ask Viktor for his commentary.

---

## Stack

- Python 3.10+
- [discord.py](https://github.com/Rapptz/discord.py) — Bot framework
- [requests](https://pypi.org/project/requests/) — For API calls to Tarkov.dev
- [openai](https://pypi.org/project/openai/) SDK v1+ — For GPT-powered replies from Viktor
- [dotenv](https://pypi.org/project/python-dotenv/) — Environment variable management
- [difflib](https://docs.python.org/3/library/difflib.html) — For fuzzy matching boss names
- [Tarkov.dev GraphQL API](https://tarkov.dev/api) — All live game data (ammo, flea market, hideout, etc.)
- JSON-based data layer for custom boss intel

---

## Project Structure

```bash
.
├── bot.py                  # Bot entry point
├── .env                    # API keys and config flags
├── requirements.txt        # Python dependencies
├── cogs/                   # Modular command handlers
│   ├── ammo.py             # !ammo and !calibers
│   ├── price.py            # !price flea market/trader data
│   ├── boss.py             # !boss command, fuzzy search + Viktor
│   ├── chat.py             # !reply and !introduce for GPT dialog
│   ├── quest.py            # !quest briefing + GPT analysis
│   ├── hideout.py          # !build and !buildlvl for hideout planning
│   └── help.py             # Custom help command
├── ai/                     # GPT prompt + response logic
│   └── relay.py            # Viktor personality and chat behavior
├── data/                   # Static game intel
│   └── bosses.json         # Handcrafted boss intel (loot, tactics, etc.)
├── logs/
│   └── bot.log             # Logging output