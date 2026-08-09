from discord import app_commands
import discord
import steam_fetch
import json

class BackLog(discord.ui.Modal, title='Feedback'):
    name = discord.ui.TextInput(
        label='Name',
        placeholder='Your name here...',
    )

    game_title = discord.ui.TextInput(
        label="Game Title:",
        placeholder='Please enter ze game title here (Genau)',
        min_length=3,
        max_length=50
    )

    feedback = discord.ui.TextInput(
        label='Why is this being added to the log?',
        style=discord.TextStyle.long,
        placeholder='Do not leave blank though!',
        default="No reasoning",
        required=False,
        max_length=300,
        min_length=2,
    )

    # Take a new game for the backlog, get the data and dump it into Json
    async def on_submit(self, interaction: discord.Interaction):
        data = steam_fetch.get_game_info(self.game_title.value)
        if (data == "failed"):
            self.on_error()

        data["reasoning"] = self.feedback.value
        temp = data["title"]
        temp_flat = data["title"].replace(' ','')
        # Checking for previous backlogging
        if steam_fetch.do_we_have_it(temp_flat):
            await interaction.response.send_message(f'{temp} is already backlogged!', ephemeral=True)
            return
        
        file_name = "../data/back_log/" + temp_flat + ".json"

        # Writing output file
        data = json.dumps(data, indent=4)
        with open(file_name, "w") as f:
            f.write(data)

        await interaction.response.send_message(f'Achtung: {self.name.value} has submitted {temp} for the backlog!')

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message('OH NEIN! Its either broken or that title already exists!', ephemeral=True)            

