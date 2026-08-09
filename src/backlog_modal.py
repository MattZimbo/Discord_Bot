from discord import app_commands
import discord

class Feedback(discord.ui.Modal, title='Feedback'):
    name = discord.ui.TextInput(
        label='Name',
        placeholder='Your name here...',
    )

    feedback = discord.ui.TextInput(
        label='What do you think?',
        style=discord.TextStyle.long,
        placeholder='Type your feedback here: ...',
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Tahnks for the feedback, {self.name.value}')

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message('Its broken.', ephemeral=True)