import discord

from discord.ext import commands
from src.database.db_connection import get_db_connection
from src.database.users import add_or_update_user

class UsersCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Slash command to register a user
    @discord.slash_command(name='register', description="Register your account with the bot")
    async def register(self, ctx: discord.ApplicationContext, username, uid):
        # Check if the command is being run in a DM
        if ctx.channel.type != discord.ChannelType.private:
            await ctx.respond("This command can only be used in a private message. Please DM me to register.", ephemeral=True)
            return

        # Use ctx.author to get Discord user information
        discord_id = ctx.author.id

        # Add or update the user in the database
        add_or_update_user(discord_id, username, uid)

        await ctx.respond(f"User '{username}' - UID '{uid}' has been registered with Discord ID {discord_id}.")


    # Helper function to send a DM for registration
    async def prompt_registration(self, user):
        try:
            await user.send("Hello! It looks like you are not registered yet. Please use `/register` to register yourself with the bot.")
        except discord.Forbidden:
            # Handle cases where the bot is unable to send a DM to the user (e.g., user has DMs turned off)
            await user.send("I couldn't send you a DM. Please ensure your privacy settings allow messages from this server's members.")


# Add the cog to the bot
def setup(bot):
    bot.add_cog(UsersCommands(bot))
