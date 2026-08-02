import os
from dotenv import load_dotenv
import discord
import debugger as DB

# Debug flag
DEBUG = True
DB.set_debug(DEBUG)

# Loading discord token from .env file
load_dotenv()

'''
Main bot class
'''
class Client(discord.Client):

    # Runs when the bot turns on
    async def on_ready(self):
        DB.Debug(f'Logged on as {self.user}!')

    # When a message is sent in the server, this is called
    async def on_message(self, message):
        DB.Debug(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

# Run bot by passing in intents obj
client = Client(intents=intents)
client.run(os.getenv("DISCORD_BOT_TOKEN"))