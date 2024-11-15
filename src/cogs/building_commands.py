import discord

from discord.ext import commands
from src.database.buildings import get_buildings, get_max_pages
from src.database.users import is_user_registered

class BuildingCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash command to get building information
    @discord.slash_command(name='building_info', description="Get information about buildings")
    async def building_info(self, ctx: discord.ApplicationContext, page: int = 1):

        # Check if the user is registered
        if not is_user_registered(ctx.author.id):
            await self.prompt_registration(ctx.author)
            await ctx.respond("You need to be registered to use this command. I've sent you a private message with further instructions.", ephemeral=True)
            return

        info = get_buildings(page)

        max_pages = get_max_pages()

         # Make sure page is within range
        if page > max_pages or page < 1:
            await ctx.respond(f"Invalid page number. Please select a page between 1 and {max_pages}.")
            return

        response_lines = []

        # Add the header
        header = f"{'Building Name':<30} {'Tier':<10} {'Max Level':<10} {'Set':<20}"
        response_lines.append(header)
        response_lines.append("-" * 80)  # Separator line

        # Format each building entry
        for building in info:
            name = building['Building Name'].ljust(30)
            tier = building['Tier'].ljust(10)
            max_level = str(building['Max Level']).ljust(10)
            set_name = building.get('Set', '').ljust(20)

            line = f"{name} {tier} {max_level} {set_name}"
            response_lines.append(line)

        # Join all lines to create the response message
        response_message = "\n".join(response_lines)

        # Add page information at the end
        page_info = f"\n\nPage {page} out of {max_pages}"
        response_message += page_info

        # Wrap the entire response in triple backticks to ensure fixed-width formatting
        response_message = f"```\n{response_message}\n```"

        # Send the formatted response
        await ctx.respond(response_message)








     # Helper function to send a DM for registration
    async def prompt_registration(self, user):
        try:
            await user.send("Hello! It looks like you are not registered yet. Please use `/register` to register yourself with the bot.")
        except discord.Forbidden:
            # Handle cases where the bot is unable to send a DM to the user (e.g., user has DMs turned off)
            await user.send("I couldn't send you a DM. Please ensure your privacy settings allow messages from this server's members.")


# Add the cog to the bot
def setup(bot):
    bot.add_cog(BuildingCommands(bot))