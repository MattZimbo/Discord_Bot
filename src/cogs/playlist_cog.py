# Discord Libs
from discord import app_commands
from discord.ext import commands
import discord
#playlist Database stuff
from database.playlist_DB import create_playlist, add_song_to_playlist

class PlaylistCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="create_playlist", description="Create a new playlist!")
    async def create_playlist(self, interaction: discord.Interaction, name: str):
            ''' Add a new playlist '''
            if (len(name) > 4):
                await interaction.response.send_message(
                    "Unfortunately that name is too short - Almost as short as Ethan. Please make it 5 characters or more.", 
                    ephemeral=True
                )
            else:
                username = str(interaction.user.name)
                results = await create_playlist(self.bot.db, str(interaction.guild_id), username, name)

                if results:
                    await interaction.response.send_message(f"Success! New playlist **{name}** created by {username}")
                else:
                    await interaction.response.send_message(f"Failure to create new playlist.")

    @app_commands.command(name="add_to_playlist", description="Add a song to a new playlist!")
    async def add_to_playlist(self, interaction: discord.Interaction, playlist_name: str, song: str):
        ''' Add a song to a playlist '''
        if (len(song) < 3):
            await interaction.response.send_message(f"Hmmmm... that seems too short. Denied.")
        else:
            results = await add_song_to_playlist(self.bot.db, str(interaction.guild_id), playlist_name, song)
            if results:
                await interaction.response.send_message(f"Adding song {song} to playlist {playlist_name}")
            else:
                await interaction.response.send_message(f"Failure to add to playlist.")
            

async def setup(bot):
    await bot.add_cog(PlaylistCog(bot))