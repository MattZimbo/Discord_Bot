# MongoDB
from motor.motor_asyncio import AsyncIOMotorDatabase

# Submit a playlist info to the database
async def create_playlist(db: AsyncIOMotorDatabase, guild_id: str, user_id: str, title: str):
    '''
    Takes a playlist name, and creates a new playlist of that name. 

    --------------------
    Params:
    --------------------
    guild_id: str
    - The ID of the guild.

    title: str
    - Title of the playlist.

    user_id: str
    - Name of the creator.
    '''

    playlist = {
            "guild_id"      : str(guild_id),
            "playlist_title": title,
            "Submitted_by"  : str(user_id),
            "songs"         : []
        }
    
    result = await db["playlists"].insert_one(document=playlist)
    return result

## This ones a doosey.
async def add_song_to_playlist(db: AsyncIOMotorDatabase, guild_id: str, title: str, song: str):
    '''
    Self explanitory.
     
    --------------------
    Params:
    --------------------
    guild_id: str
    - ID of the guild

    title: str
    - title of the playlist

    song: str
    - name of the song
    '''
    #addToSet adds one if theres not one there
    results = await db["playlists"].update_one({"guild_id": guild_id, "playlist_title": title}, {"$addToSet": {"songs": { "title": song}}})
    return results