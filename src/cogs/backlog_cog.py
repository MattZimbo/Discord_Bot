# Discord Libs
from discord import app_commands
from discord.ext import commands
import discord
from discord.utils import MISSING
# Scripts
import components.steam_fetch as steam_fetch
from database.backlog_DB import submit_game_info, get_server_games, remove_game

'''
------------------- MODAL UI -------------------------
'''

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
        data = await steam_fetch.get_game_info(self.db, str(interaction.guild_id), self.game_title.value, self.reasoning.value)
        print(data)
        if (data == "failed"):
            return await interaction.response.send_message(f"This game is already in the backlog! Move along - Move along...", ephemeral=True)

        # Logic to check if we already have it
        await submit_game_info(self.db, str(interaction.guild_id), str(interaction.user.id), data)
        await interaction.response.send_message(f'Game information for {data["title"]} added to the backlog by {interaction.user.name}!')

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(f"User ran into an error: {error}")
        await interaction.response.send_message('OH NEIN! Its broken again! Vhat on earth did you try to backlog?', ephemeral=True)

'''
------------------- VIEW MESSAGE UI -------------------------
'''

class DeleteBackLog(discord.ui.View):
    def __init__(self, options_list, db):
        super().__init__(timeout=10)
        self.db = db

        #NOTE:  Discord allows up to 25 options
        select_options = [ discord.SelectOption(label=game, value=game) for game in options_list[:25] ]

        self.select = discord.ui.Select(
            placeholder="Choose a game to remove: ",
            options=select_options,
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        selected_game = self.select.values[0]

        # Disable and delete
        self.select.disabled = True
        self.stop()

        ## Call remove function here.
        await remove_game(self.db, str(interaction.guild_id), selected_game)
        await interaction.response.send_message(f"Successfully deleted **{selected_game}** from your backlog!")

'''
------------------- ACTUAL COG -------------------------
'''

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
                    embed.add_field(name="%: ", value="%" + game["discount_%"],inline=True)
                else:
                    embed.add_field(name="Discounted: ", value=":x:",inline=False)

            embed.add_field(name="Description: ",value=game["reasoning"], inline=False)

            await interaction.followup.send(embed=embed)

    ## Remove a game from the backlog
    @app_commands.command(name= "remove_backlog", description='Remove a game from the backlog')
    async def delete_backlog(self, interaction: discord.Interaction):
        
        user_games = await get_server_games(self.bot.db, str(interaction.guild_id))

        if not user_games:
            return await interaction.response.send_message("No games submitted yet!")

        title_list = [f"{g["title"]}" for g in user_games]
        view = DeleteBackLog(title_list, self.bot.db)
        await interaction.response.send_message("Select a game to remove:", view=view, ephemeral=True)

# Load the BackLogCog
async def setup(bot):
    await bot.add_cog(BacklogCog(bot))