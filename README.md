# H.A.N.S
- Helpful
- Architectured
- (Not-An-Evil-Robot)
- Systems

## Description:
An asynchronous Discord application built with Python, featuring multi-tenant server settings, dynamic game price tracking across global regions, and audio streaming via Lavalink. Fully containerised with Docker Compose for seamless deployment.

---

### Features:
- **Audio Streaming:** Utilizes a dedicated Lavalink node alongside Python's `Wavelink` library to process, stream, and manage audio queues via URL or query searches with minimal latency.

- **Game Backlogging:** The bot is able to take a game title, call upon the Steam Store API and extract that the game that is most relevant to the title and its information; such as the title, price tag across 3 different regions (South Africa, Europe, USA), current discount percentage and discount indicator, and the games generic thumbnail. Users can print out the backlog or add and delete games at any moment. The games are stored in MongoDB. Please refere to the Database schema section for the Schema.

- **Playlists (In progress):** The bot is able to take a new playlist name to create and store a playlist on MongoDB. Users can then add or remove specific songs from individual playlists, and delete playlists as a whole. Please refere to the Database schema section for the Schema.

- **Server-Specific Backlogs & Playlists:** Persists structured user backlogs and custom server playlists to MongoDB, ensuring isolated state management per Discord Guild.

- **Full Containerization:**: Packaged with Docker Compose to orchestrate both the Python bot runtime and the Lavalink Java audio service in isolated environments.

---

## Tech Stack

* **Language:** Python 3.10+ (`asyncio`, `discord.py`)
* **Database:** MongoDB (Motor / PyMongo)
* **Audio Server:** Lavalink / Wavelink
* **Containerization:** Docker, Docker Compose
* **External APIs:** Steam Store API

---
## Architecture & Database Schemas

Data is isolated by `guild_id` to ensure secure multi-tenant usage across Discord servers.

### 1. `server_settings` Collection
| Field | Type | Description |
| :--- | :--- | :--- |
| `guild_id` | `String` | Unique Discord Server Snowflake ID |
| `guild_name` | `String` | Registered server name |
| `joined_date` | `DateTime` | Bot installation timestamp |
| `log_channel_id` | `String` | Designated audit log channel ID |
| `welcome_channel_id`| `String` | Designated onboarding channel ID |

### 2. `backlogs` Collection
| Field | Type | Description |
| :--- | :--- | :--- |
| `guild_id` | `String` | Discord Server Snowflake ID |
| `submitted_by` | `String` | Discord User ID of contributor |
| `title` | `String` | Steam catalog title |
| `game_img` | `String` | URL to Steam thumbnail asset |
| `price_usd` | `Float` | Localized price (USD) |
| `price_eur` | `Float` | Localized price (EUR) |
| `price_zar` | `Float` | Localized price (ZAR) |
| `is_discounted` | `Boolean` | Current sale status flag |
| `discount_pct` | `Integer` | Discount percentage value |
| `is_free` | `Boolean` | Free-to-play status flag |
| `reasoning` | `String` | User submission note/context |

### 3. `playlists` Collection
| Field | Type | Description |
| :--- | :--- | :--- |
| `guild_id` | `String` | Discord Server Snowflake ID |
| `playlist_title` | `String` | User-defined playlist name |
| `submitted_by` | `String` | Discord User ID of creator |
| `songs` | `Array[String]`| List of track identifiers/URLs |

---

## Repository structure
```text
├── docker-compose.yml
├── Dockerfile
├── lavalink
│   └── application.yml
├── README.md
├── requirements.txt
├── run.sh
├── setup.sh
└── src
    ├── cogs
    │   ├── backlog_cog.py
    │   ├── playlist_cog.py
    │   └── voice_cog.py
    ├── components
    │   ├── debugger.py
    │   └── steam_fetch.py
    ├── database
    │   ├── backlog_DB.py
    │   └── playlist_DB.py
    └── main.py
```
---

## Important running information:
1) Fill out the information in the `.env`
2) Run `./setup` to install all required dependancies
3) Run `run.sh` to launcher the docker

## RoadMap:
1) [x] Steam API Integration & Multi-Currency Aggregation
2) [x] Lavalink Voice Streaming Integration
3) [ ] Batch addition/removal for custom playlist tracks
4) [ ] Guild event Handler (Dynamic Welcomer & Help commands)
5) [ ] Administrative capabilities and audit logging engine

---

## Git commit Key
### Start with the "Title" followed by:
- "[NOTE] _description of commit_" --> Only when necessary to denote specific details.
- "[+] _description of feature_" --> A feature was added / improved.
- "[-] _description of feature_" --> A feature was removed/ reduced.
- "[%] _description of feature_" --> A feature was modified/ Changed.