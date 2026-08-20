# H.A.N.S
- Helpful
- Architectured
- (Not-An-Evil-Robot)
- Systems
## Author:
- Mattzimbo

## Important running information:
1) Fill out the information in the `.env`
2) Run `./setup` to install all required dependancies
3) Run `run.sh` to launcher the docker

## Description:
A simplistic `Discord Bot` built to entertain members of my server through the Discord API and Python Asyncio. It utilises a non-relation database (MongoDB) to store and interact with individual server information for certain features, whilst using lavalink and wavelink to enable the bot to play music. The bot can also extract detailed information about video games that a user wants to backlog by calling the Steam Store APIs. This is primarily used when adding games to the game backlog. Please find a more apt description of features below:

### Features:
- Music Playing:
    Through a combination of Lavalink and Pythons Wavelink module, the bot is able to process and play different songs based off of an input URL or title under the slash command "/play".

- Game Backlogging:
    The bot is able to take a game title, call upon the Steam Store API and extract that the game that is most relevant to the title, and display information relation to said game, such as the title, price tag across 3 different regions (South Africa, Europe, USA), current sale percentage and sale indicator, and the games generic thumbnail. Users can print out the backlog or add and delete games at any moment. The games are stored in MongoDB. Please refere to the Database schema section for the Schema.

- Playlists (In progress):
    The bot is able to take a new playlist name to create and store a playlist on MongoDB. Users can then add or remove specific songs from individual playlists, and delete playlists as a whole. Please refere to the Database schema section for the Schema.

- Misc Slash commands:
    A variety of slash commands exist with differentiated purposes, mostly for entertainment.

- Dockerisation:
    The bot is completely dockerised, and able to run on a multitude of platforms.

## RoadMap:
1) Finish implementation of playlists by adding the ability to add multiple songs at once
2) Setup the Bots welcoming functionality and help message.
3) Setup the Bots logging functionality to track user actions in a server for admin review
4) TBD.

## Mongo Database Schema:  
- Server_settings schema:  
{  
  guild_id: '{discord ID}',         --> Identifier of the server  
  guild_name: '{discord Name}',     --> Servers Name at the time of join  
  joined_date: '{DateTime}',        --> DateTime that the bot joined a server  
  log_channel_id: {discord ID},     --> ID of the server's logging chanel  
  welcome_channel_id: {discord ID}  --> ID of the server's welcome chanel  
}

- Backlog Schema:  
{   
  guild_id: '{discord ID}',     --> Identifier of the server it was created in  
  Submitted_by: '{discord ID}', --> Identifier of the player who submitted it  
  title: '{str}',               --> Game title  
  game_img: '{url}',            --> Link to game thumbnail  
  price_USD: '${float}',        --> Price in USD  
  price_EUR: '€{float}',        --> Price in Euro  
  price_ZAR: 'R{float}',        --> Price in Rand  
  is_discounted: true,          --> Discount indicator  
  'discount_%': '{int}',        --> Discount percentage  
  is_free: false,               --> Denotes where the game is free  
  reasoning: '{str}'            --> Reason the player added the game to the backlog  
}

- Playlist Schema (In progress):  
{  
  guild_id: '{discord ID}',     --> Identifier of the server it was created in  
  playlist_title: '{str}',      --> Name of the playlist  
  Submitted_by: '{discord ID}', --> Identifier of the player who submitted it  
  songs: [                      --> List of Songs in playlist  
    {  
      title: '{str}'            --> Song titles  
    }  
  ]  
}


## Repository structure
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
    │   └── voice_cog.py
    ├── components
    │   ├── debugger.py
    │   └── steam_fetch.py
    ├── database
    │   └── backlog_DB.py
    └── main.py

## Git Key
### Start with the "Title" followed by:
- "[NOTE] _description of commit_" --> Only when necessary to denote specific details.
- "[+] _description of feature_" --> A feature was added / improved.
- "[-] _description of feature_" --> A feature was removed/ reduced.
- "[%] _description of feature_" --> A feature was modified/ Changed.

## ------ Personal notes --------

## Running LavaLink
### IPV6 rotation:
- sudo sysctl -w net.ipv6.ip_nonlocal_bind=1
- (To make it permanent run) echo "net.ipv6.ip_nonlocal_bind = 1" | sudo tee -a /etc/sysctl.conf

## Using docker
### Starting:
- docker compose up --build
### Clean shutdown and cache remove
- docker compose down