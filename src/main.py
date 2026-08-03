import os
import sys
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord import app_commands

import debugger as DB

# Debug flag
DEBUG = True
DB.set_debug(DEBUG)

# Loading discord token from .env file
load_dotenv()

'''
Main bot class
'''
class Client(commands.Bot):

    # Runs when the bot turns on
    async def on_ready(self):
        DB.Debug(f'Logged on as {self.user}!')

        # Force load slash commands
        try:
            guild = discord.Object(id=os.getenv("DISCORD_SERVER_ID"))
            synced = await self.tree.sync(guild=guild)
            DB.Debug(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            DB.Debug(f'Error syncing commands: {e}')


    # When a message is sent in the server, print the content and sender
    async def on_message(self, message):
        # ignore self
        if message.author == self.user:
            return

        if message.content.startswith('hello'):
            await message.channel.send(f"Hi there {message.author}")

        DB.Debug(f'Message from {message.author}: {message.content}')

    # When a user reacts to an event
    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send(f'You reacted with {reaction}')
        DB.Debug(f'Reaction from {user} with {reaction}')

    # Triggers when a user joins
    async def on_member_join(self, member):
        # channel = bot.get_channel(CHANNEL_WELCOME)
        # await channel.send(f"Welcome to the server, {member.mention}!")
        DB.Debug(f'Member joined: {member}')


intents = discord.Intents.default()
intents.message_content = True

# NOTE: Command prefixs are redundant, but required in the code for some reason.
client = Client(command_prefix=";", intents=intents)

'''
-----------------------------------------------------
----------------- SLASH COMMANDS --------------------
-----------------------------------------------------
'''
# Specify our server to prevent propegation
try:
    GUILD_ID = discord.Object(id=os.getenv("DISCORD_SERVER_ID"))
except Exception as e:
    DB.Debug(f"Server ID malfunction. Double check ID. Error {e}")
    sys.exit()

# Default Respond to hello
@client.tree.command(name="hello", description="Says Good-en-tag", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Good-en-tag!")

# Default print out something (Example of arguements)
@client.tree.command(name="print", description="I'll say anything", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction, printer:str):
    await interaction.response.send_message(printer)

'''
----------------- Embed stuff --------------------
'''
# Default Embed (Think of a form - title, fields ect)
@client.tree.command(name="embed", description="Embed example", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    embed = discord.Embed(title="I am a Title", url="https://www.google.com/", description="I am the description", colour=discord.Colour.gold())
    embed.set_thumbnail(url="https://img.icons8.com/?size=100&id=12580&format=png&color=000000")
    embed.add_field(name="Game Title:", value="The game name", inline=False)
    embed.add_field(name="Personal rating:", value="The game rating", inline=False)
    embed.add_field(name="Original Price:", value="FREE")
    embed.set_footer(text="Requires a minimum of 2 Green tick reactions")
    embed.set_author(name=interaction.user.name)
    await interaction.response.send_message(embed=embed)

'''
----------------- Button stuff --------------------
'''
class View(discord.ui.View):
    @discord.ui.button(label="display_text", style=discord.ButtonStyle.green)
    async def button_callback(self, button, interaction):
        await button.response.send_message("Test button pressed.")

    # Can put more buttons in here and set the class name to something else.

# Default Button testing
@client.tree.command(name="button", description="button test", guild=GUILD_ID)
async def myButton(interaction: discord.Interaction):
    await interaction.response.send_message(view=View())

# Run the bot
client.run(os.getenv("DISCORD_BOT_TOKEN"))