import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
import random

# YTDL Configuration for extraction
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

class VoiceCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="join", description="Makes Hans join your voice channel")
    # This function controls the voice channel hans is in
    async def join(self, interaction: discord.Interaction):
        if not interaction.user.voice or not interaction.user.voice.channel:
            return await interaction.response.send_message("You need to be in a voice channel first Dumpfbacke", ephemeral=True)

        # Channel switching
        channel = interaction.user.voice.channel
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(channel)
            await interaction.response.send_message(f"Moved to {channel.name}!")
        else:
            await channel.connect()
            await interaction.response.send_message(f"Joined {channel.name}!")


      
    # Make hans leave a voice channel
    @app_commands.command(name="leave", description="Sends my soul back into the Abyss")
    async def leave(self, interaction: discord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            ranint = random.randint(0,3)
            # Random leave message
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



    # Make Hans play music
    @app_commands.command(name="play", description="Play audio from a URL or YouTube search")
    async def play(self, interaction: discord.Interaction, query: str):
        if not interaction.user.voice or not interaction.user.voice.channel:
            return await interaction.response.send_message("You must be in a voice channel to play music WarmDuscher", ephemeral=True)

        await interaction.response.defer()

        voice_client = interaction.guild.voice_client
        if not voice_client:
            voice_client = await interaction.user.voice.channel.connect()
        elif voice_client.channel != interaction.user.voice.channel:
            await voice_client.move_to(interaction.user.voice.channel)

        if voice_client.is_playing():
            voice_client.stop()

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url']
        title = data.get('title', 'Audio Track')

        source = discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS)
        voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await interaction.followup.send(f'🎶 Now playing: **{title}**')

    @app_commands.command(name="stop", description="Stops the currently playing music")
    async def stop(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message('Stopped the music - ::')
        else:
            await interaction.response.send_message('Nothing is currently playing.', ephemeral=True)


# This setup function is required for extension loading
async def setup(bot):
    await bot.add_cog(VoiceCog(bot))