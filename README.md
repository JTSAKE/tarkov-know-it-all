# Tarkov Know-It-All Bot — "Viktor 'Relay' Antonov"

A Discord bot built for Escape From Tarkov players. Viktor is more than a bot — he's your squad's embedded PMC intel specialist. Tactical, sarcastic, and occasionally offensive (in Russian, with translations). This project combines real-time game data with OpenAI to deliver immersive, role-play-driven squad support.

---

## 🧰 Current Features

### ✅ Core Framework
- Modular command structure using Discord.py cogs
- Error handling & logging
- Custom `!help` command (in-character)
- Dev mode heartbeat + debug toggles
- `.env` support and secure API key loading

---

### 🔫 `!ammo <caliber>`
Fetches real-time ammo data from the [Tarkov.dev](https://tarkov.dev) API and sends it through OpenAI's GPT model.

- Returns top-performing ammo by penetration
- Supports fuzzy aliases (e.g., `!ammo 9x19`)
- Viktor gives a tactical, sarcastic ammo briefing
- GPT-driven personality in full effect

---

### 🎯 `!calibers`
- Returns a list of supported ammo calibers
- Response is in-character from Viktor
- Delivered with attitude and a jab or two for even asking

---

### 💰 `!price <item name>`
Fetches flea market and trader prices for any item.

- Uses fuzzy matching (`gpu` → `Graphics Card`)
- Live pricing from Tarkov.dev (24h average, low, trader offers)
- GPT formats the data into a short, snarky market analysis
- Viktor tells you if it's “worth dying for” or “trader trash”

---

### 🛠️ `!build <module name>`
Returns all requirements to build or upgrade a hideout module.
Fuzzy-matches hideout station names (bitcoin, medstation, water, etc.)
Shows item counts, skill levels, and prerequisite modules for each level
Pulls real-time data from Tarkov.dev's hideout structure
Future-ready for Viktor to critique your base-building priorities

---

### 🧱 `!buildlvl <module name>`
Lists all upgrade levels available for a given hideout module.
Fuzzy-matches hideout station names (lavatory, intel, med, etc.)
Displays available levels in a clean list (e.g., Lv1, Lv2, Lv3)
Useful for planning what’s possible before gathering materials
Viktor adds commentary about your ambitions (or lack thereof)

---

## 🧠 Viktor: The Personality

Viktor "Relay" Antonov is a grizzled, ex-military AI advisor.

- Built using OpenAI’s `gpt-4`
- Responses shaped by system and user prompt engineering
- Drops occasional Russian insults (with *English translations*)
- Never breaks character. Ever.

---

## 🚀 Planned Features

- `!boss <map>`: Location intel, spawn chances, Viktor commentary
- `!extracts <map>`: Accessible extract info
- `!price <multi-item>`: Batch price queries
- `!quest <name>`: Briefings and progression tracking
- Viktor mood modes (`!viktormode chill`, `!viktormode brutal`)
- Cooldown system + GPT query caching

---

## 🛠️ Stack

- Python 3.10+
- Discord.py
- Requests
- OpenAI SDK (v1+)
- Tarkov.dev GraphQL API
- dotenv

---

## 👥 For the Squad (Eventually)
Currently built for internal squad use, but may be open-sourced in the future. Designed to scale from utility bot → immersive squadmate → full PMC toolkit.

---

## 📁 Project Structure

```bash
.
├── bot.py                # Entry point
├── .env                  # API keys and dev flags
├── cogs/
│   ├── ammo.py           # !ammo and !calibers
│   ├── price.py          # !price intel
│   └── help.py           # Custom help command
├── ai/
│   └── relay.py          # GPT integration and prompt engineering
├── logs/
│   └── bot.log           # Logging output
