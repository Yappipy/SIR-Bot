from discord.ext import commands
from src.database.db_connection import get_db_connection

class StatsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stats')
    async def stats(self, ctx):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT messages_sent FROM users WHERE user_id=?", (ctx.author.id,))
        user = c.fetchone()
        conn.close()

        if user:
            await ctx.send(f'{ctx.author.name}, you have sent {user[0]} messages!')
        else:
            await ctx.send(f'{ctx.author.name}, I have no record of your messages.')

# Add the cog to the bot
def setup(bot):
    bot.add_cog(StatsCommands(bot))
