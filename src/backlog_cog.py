# Discord Libs
from discord import app_commands
from discord.ext import commands
import discord
from discord.utils import MISSING
# Scripts
import steam_fetch
from DB_backlog import submit_game_info, get_server_games

class BackLog(discord.ui.Modal, title='BackLog adder'):

    game_title = discord.ui.TextInput(
        label="Game Title:",
        placeholder='Please enter ze game title here (Genau)',
        min_length=3,
        max_length=50
    )

    reasoning = discord.ui.TextInput(
        label='Why is this being added to the log?',
        style=discord.TextStyle.long,
        placeholder='Do not leave blank though!',
        default="No reasoning",
        required=False,
        max_length=300,
        min_length=2,
    )

    def __init__(self, db):
        super().__init__()
        self.db = db

    # Take a new game for the backlog, and add it to the database.
    async def on_submit(self, interaction: discord.Interaction):
        data = steam_fetch.get_game_info(self.game_title.value, self.reasoning.value)
        if (data == "failed"):
            self.on_error()

        # Logic to check if we already have it
        await submit_game_info(self.db, str(interaction.guild_id), str(interaction.user.id), data)
        await interaction.response.send_message(f'Game information for {data["title"]} retrieved successfully!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message('OH NEIN! Its either broken or that title already exists!', ephemeral=True)

class BacklogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ''' Add game to backlog '''
    @app_commands.command(name="backlog", description='submit a game to the backlog')
    async def backlog(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BackLog(self.bot.db))

    ''' Print out the backlog '''
    @app_commands.command(name="print_backlog", description="I'll spit out your current backlog")
    async def sayPrint(self, interaction: discord.Interaction):
        await interaction.response.send_message("Printing ze backlog...")
        all_games = await get_server_games(self.bot.db, str(interaction.guild_id))
        for game in all_games:
            embed = discord.Embed(title=game["title"], url=game["url"], colour=discord.Colour.gold())
            embed.set_thumbnail(url=game["game_img"])

            if (game["is_free"]):
                embed.add_field(name="Price:", value="FREE", inline=True)
            else:
                embed.add_field(name="USD Price:", value=game["price_USD"], inline=True)
                embed.add_field(name="EUR Price:", value=game["price_EUR"], inline=True)
                embed.add_field(name="ZAR Price:", value=game["price_ZAR"], inline=True)
                if (game["is_discounted"]):
                    embed.add_field(name="Discounted: ", value=":white_check_mark:",inline=True)
                    embed.add_field(name="%: ", value="%" + game["discount %"],inline=True)
                else:
                    embed.add_field(name="Discounted: ", value=":x:",inline=False)

            embed.add_field(name="Description: ",value=game["reasoning"], inline=False)

            await interaction.followup.send(embed=embed)

# Load the BackLogCog
async def setup(bot):
    await bot.add_cog(BacklogCog(bot))