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
        await member.message.channel.send(f'Welcome in {member}')
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

# Run the bot
client.run(os.getenv("DISCORD_BOT_TOKEN"))