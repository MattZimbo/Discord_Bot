import discord
from discord import app_commands
import backlog_printer

class DeleteBackLog(discord.ui.View):
    def __init__(self, options_list):
        super().__init__(timeout=10)

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

        backlog_printer.deleted_log(selected_game)
        await interaction.response.send_message(f"Successfully deleted **{selected_game}** from your backlog!")