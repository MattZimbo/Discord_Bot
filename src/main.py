# Default libraries + Dotenv
import os
import sys
from dotenv import load_dotenv
load_dotenv()
# Discord libs
import discord
from discord.ext import commands
from discord import app_commands
# MongoDB
import motor.motor_asyncio
# Scripts
from backlog_modal import BackLog
import backlog_printer
from view_messages import DeleteBackLog
import debugger as DB


# Debug flag
DEBUG = True
DB.set_debug(DEBUG)



'''
Main bot class
'''
class Client(commands.Bot):

    # Run pre-ready processes.
    async def setup_hook(self):
        # Database setup
        Password = os.getenv("MONGO_DB_PASSWORD")
        Username = os.getenv("MONGO_DB_USERNAME")
        uri = f"mongodb+srv://{Username}:{Password}@hansdb.s0wgibr.mongodb.net/?appName=HansDB"
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.mongo_client["HansDB"]

        await self.load_extension("voice_cog")
        DB.Debug("Loaded VoiceCog extension successfully.")

    # Runs when the bot turns on
    async def on_ready(self):
        DB.Debug(f'Logged on as {self.user}!')

        # Force load slash commands for every guild avaliable
        try:
            for guild in self.guilds:
                guild_obj = discord.Object(id=guild.id)
                self.tree.copy_global_to(guild=guild_obj)
                synced = await self.tree.sync(guild=guild_obj)
                DB.Debug(f'Synced {len(synced)} commands to guild {guild.name} {guild.id}')
                # If we ever get more than persay 5 servers, do synced = await self.tree.sync() for global sync
            
        except Exception as e:
            DB.Debug(f'Error syncing commands: {e}')

        # Ensure all servers we are on are registered
        # If not, register them.
        collection = self.db["server_settings"]
        for guild in self.guilds:
            default_settings = {
                "guild_id"              : str(guild.id),
                "guild_name"            : guild.name,
                "welcome_channel_id"    : None,
                "log_channel_id"        : None,
                "joined_date"           : guild.me.joined_at.isoformat()
            }

            await collection.update_one(
                {"guild_id": str(guild.id)},
                # $setOnInsert doesn't overwrite old settings if they exist.
                {"$setOnInsert": default_settings},
                upsert=True
            )
        print("Checked and initilised all server settings.")


    # When a message is sent in the server, print the content and sender
    async def on_message(self, message):
        # ignore self
        if message.author == self.user:
            return

        if message.content.startswith('Hans'):
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

    # Close mongo_DB connections
    async def close(self):
        self.mongo_client.close()
        await super().close()

    # Add new servers contents to MONGO
    async def on_guild_join(self, guild: discord.Guild):
        collection = self.db["server_settings"]

        # Set the default settings of every server.
        default_settings = {
            "guild_id"              : str(guild.id),
            "guild_name"            : guild.name,
            "welcome_channel_id"    : None,
            "log_channel_id"        : None,
            "joined_date"           : guild.me.joined_at.isoformat()
        }

        await collection.update_one(
            {"guild_id": str(guild.id)},
            # $setOnInsert doesn't overwrite old settings if they exist.
            {"$setOnInsert": default_settings},
            upsert=True
        )

        print(f"Initialized settings for new server: {guild.name} ({guild.id})")


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
async def sayPrint(interaction: discord.Interaction, printer:str):
    await interaction.response.send_message(printer)

# Shutdown the bot -- Testing only
@client.tree.command(name="shutdown", description="Vhat is this?", guild=GUILD_ID)
@app_commands.default_permissions(administrator=True)
async def killProcess(interaction: discord.Interaction):
    await interaction.response.send_message("**NEIN, NEIN, NEIN, NEIN, NEIN! FASS DAS NICHT AN, DU VOLLIDIOT, ODER ICH...**")
    sys.exit()

'''
----------------- Embed stuff --------------------
'''
# Default Embed (Think of a form - title, fields ect)
@client.tree.command(name="embed", description="Embed example", guild=GUILD_ID)
async def sayEmbed(interaction: discord.Interaction):
    embed = discord.Embed(title="I am a Title", url="https://www.google.com/", colour=discord.Colour.gold())
    embed.set_thumbnail(url="https://img.icons8.com/?size=100&id=12580&format=png&color=000000")
    embed.add_field(name="Game Title:", value="The game name", inline=True)
    embed.add_field(name="Personal rating:", value="The game rating", inline=False)
    embed.add_field(name="Original Price:", value="FREE", inline=True)
    embed.add_field(name="Discounted: ", value=":white_check_mark:",inline=False)
    embed.set_footer(text="Requires a minimum of 2 Green tick reactions")
    embed.set_author(name=interaction.user.name)
    await interaction.response.send_message(embed=embed)

## Print out the backlog
@client.tree.command(name="print_backlog", description="I'll spit out your current backlog", guild=GUILD_ID)
async def sayPrint(interaction: discord.Interaction):
    await interaction.response.send_message("Printing ze backlog...")
    all_games = backlog_printer.get_backlog_info()
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
                embed.add_field(name="%: ", value=game["discount %"],inline=True)
            else:
                embed.add_field(name="Discounted: ", value=":x:",inline=False)

        embed.add_field(name="Description: ",value=game["reasoning"], inline=False)

        await interaction.followup.send(embed=embed)

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

'''
----------------- Modal stuff --------------------
'''
@client.tree.command(guild=GUILD_ID, description='submit a game to the backlog')
async def backlog(interaction: discord.Interaction):
    await interaction.response.send_modal(BackLog())

'''
----------------- view messages --------------------
'''

@client.tree.command(guild=GUILD_ID, description='Delete a game from the backlog')
async def delete_backlog(interaction: discord.Interaction):
    user_games = backlog_printer.get_list()

    view = DeleteBackLog(user_games)
    await interaction.response.send_message("Select a game to remove:", view=view, ephemeral=True)


# Run the bot

##async def setup(bot):
  #await bot.add_cog(VoiceCog(bot))

client.run(os.getenv("DISCORD_BOT_TOKEN"))