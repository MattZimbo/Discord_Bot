# MongoDB
from motor.motor_asyncio import AsyncIOMotorDatabase

# Submit a game to the DB
async def submit_game_info(db: AsyncIOMotorDatabase, guild_id: str, user_id: str, game_data: dict):
    game = {
        "guild_id"      : str(guild_id),
        "Submitted_by"  : str(user_id),
        **game_data
    }

    result = await db["backlog"].insert_one(document=game)
    return result.inserted_id

# Get the full backlog for a server from DB
async def get_server_games(db: AsyncIOMotorDatabase, guild_id: str):
    cursor = db["backlog"].find({"guild_id" : str(guild_id)})
    return await cursor.to_list()

# Remove a game from the backlog
async def remove_game(db: AsyncIOMotorDatabase, guild_id: str, title: str):
    await db["backlog"].delete_one({"guild_id": str(guild_id), "title": title})

