import discord
from discord.ext import commands
import os
from src.config import TOKEN
from src.database.db_connection import initialize_database, import_csv_to_database

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Set up bot with both prefix and slash commands
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("This command does not exist.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You missed a required argument for this command.")
    else:
        await ctx.send("An error occurred. Please try again later.")
        raise error  # Log it for debugging purposes

# Load cogs (commands)
def load_cogs(bot):
    bot.load_extension('src.cogs.basic_commands')
    bot.load_extension('src.cogs.stats_commands')
    bot.load_extension('src.cogs.building_commands')
    bot.load_extension('src.cogs.user_commands')
    #bot.load_extension('src.events.on_message')

# Event for when bot is ready
@bot.event
async def on_ready():

    # Sync commands to make sure slash commands are registered
    await bot.sync_commands()

    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

def run_bot():
    # Initialize the database
    initialize_database()

    import_csv_to_database('buildings', 'data/buildings.csv')
    import_csv_to_database('building_values', 'data/value.csv')

    # Load commands and events
    load_cogs(bot)

    # Run the bot
    bot.run(TOKEN)
