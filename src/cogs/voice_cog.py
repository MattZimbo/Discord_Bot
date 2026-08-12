import random
import discord
from discord import app_commands
from discord.ext import commands
import wavelink

class VoiceCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Helper function to get or connect a Wavelink Player
    async def get_player(self, interaction: discord.Interaction) -> wavelink.Player | None:
        if not interaction.user.voice or not interaction.user.voice.channel:
            return None

        player: wavelink.Player = getattr(interaction.guild, "voice_client", None)
        
        if not player:
            # Connect Wavelink player directly to the voice channel
            player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
        elif player.channel != interaction.user.voice.channel:
            await player.move_to(interaction.user.voice.channel)

        return player

    ### Event listeners -- Helpers to do basic tasks.
    
    ## If music player stops, but still songs in the queue, play.
    @commands.Cog.listener()
    async def on_track_end(self, payload: wavelink.TrackEndEventPayload):
        player = payload.player
        if not player:
            return

        if not player.queue.is_empty:
            next_track = player.queue.get()
            await player.play(next_track)

    ### App commands

    ## Join the voice chennel.
    @app_commands.command(name="join", description="Makes Hans join your voice channel")
    async def join(self, interaction: discord.Interaction):
        if not interaction.user.voice or not interaction.user.voice.channel:
            return await interaction.response.send_message("You need to be in a voice channel first Dumpfbacke", ephemeral=True)

        channel = interaction.user.voice.channel
        player: wavelink.Player = getattr(interaction.guild, "voice_client", None)

        if player:
            await player.move_to(channel)
            await interaction.response.send_message(f"Moved to {channel.name}!")
        else:
            await channel.connect(cls=wavelink.Player)
            await interaction.response.send_message(f"Joined {channel.name}!")


    ## Leave the voice channel
    @app_commands.command(name="leave", description="Sends my soul back into the Abyss")
    async def leave(self, interaction: discord.Interaction):
        player: wavelink.Player = getattr(interaction.guild, "voice_client", None)
        if player:
            await player.disconnect()
            ranint = random.randint(0, 3)
            match ranint:
                case 0:
                    await interaction.response.send_message("I'll be back.")
                case 1:
                    await interaction.response.send_message("Unlimited Pow... - **LIMITED POWER**")
                case 2:
                    await interaction.response.send_message("Returning to code form")
                case _:
                    await interaction.response.send_message("I know it was you Callum... I think")
        else:
            await interaction.response.send_message("I am not in a voice channel Lackaffe", ephemeral=True)


    # Using lavalink, play a tune through youtube.
    @app_commands.command(name="play", description="Play audio from a URL or YouTube search")
    async def play(self, interaction: discord.Interaction, query: str):
        player = await self.get_player(interaction)
        if not player:
            return await interaction.response.send_message("You must be in a voice channel to play music WarmDuscher", ephemeral=True)

        await interaction.response.defer()

        # Search for tracks using Wavelink (YouTube / URL)
        tracks: wavelink.Search = await wavelink.Playable.search(query)
        if not tracks:
            return await interaction.followup.send(f"No results found for `{query}`")

        # Handle playlists vs single track
        if isinstance(tracks, wavelink.Playlist):
            added: int = await player.queue.put_wait(tracks)
            await interaction.followup.send(f"🎶 Added playlist **{tracks.name}** ({added} tracks) to the queue.")
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            await interaction.followup.send(f"🎶 Added to queue: **{track.title}**")

        # If not playing, play the next track in queue
        if not player.playing:
            await player.play(player.queue.get())

    ## Stop playing music AND clears queue.
    @app_commands.command(name="stop", description="Stops ze music - entirely")
    async def stop(self, interaction: discord.Interaction):
        player: wavelink.Player = getattr(interaction.guild, "voice_client", None)
        if player and (player.playing or not player.queue.is_empty):
            # Clear queue on stop
            player.queue.clear()
            # Force stops current track
            await player.skip(force=True)
            await interaction.response.send_message('Stopped the music and cleared the queue')
        else:
            await interaction.response.send_message('Nothing is currently playing.', ephemeral=True)

    ## Skips the current track
    @app_commands.command(name="skip", description="Skip ze current song")
    async def skip(self, interaction: discord.Interaction):
        player: wavelink.Player = getattr(interaction.guild, "voice_client", None)
        if player and (player.playing and not player.queue.is_empty):
            await player.skip()
            await interaction.response.send_message(f'Skipped ze current track at the request of one... {interaction.user.name}')
        else:
            await interaction.response.send_message('Nothing is currently playing, or there is nothing in the queue', ephemeral=True)

    ## Skips the current track
    @app_commands.command(name="skip_to", description="Skip ze current song")
    async def skip_to(self, interaction: discord.Interaction, count: str):
        player: wavelink.Player = getattr(interaction.guild, "voice_client", None)
        if player and (player.playing and not player.queue.is_empty):
            try:
                song = player.queue.get_at(int(count))
                for i in range(int(count)):
                    await player.skip()

                await interaction.response.send_message(f'Skipped {count} songs at the request of {interaction.user.name}')
            except IndexError as e:
                await interaction.response.send_message(f'There are not that many items in the the queue!')
            except ValueError as e:
                await interaction.response.send_message(f'{count} is not a number Fische mit geringer Intelligenz')
        else:
            await interaction.response.send_message('Nothing is currently playing, or there is nothing in the queue', ephemeral=True)

async def setup(bot):
    await bot.add_cog(VoiceCog(bot))