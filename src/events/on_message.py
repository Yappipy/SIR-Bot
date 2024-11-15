from discord.ext import commands
from src.database.db_connection import get_db_connection

class MessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     # Avoid the bot responding to itself
    #     if message.author == self.bot.user:
    #         return

    #     # Log the message to the database
    #     conn = get_db_connection()
    #     c = conn.cursor()
    #     c.execute("SELECT * FROM users WHERE user_id=?", (message.author.id,))
    #     user = c.fetchone()

    #     if user is None:
    #         c.execute("INSERT INTO users (user_id, username, messages_sent) VALUES (?, ?, ?)",
    #                   (message.author.id, message.author.name, 1))
    #     else:
    #         c.execute("UPDATE users SET messages_sent = messages_sent + 1 WHERE user_id=?", (message.author.id,))
        
    #     conn.commit()
    #     conn.close()

    #     # Allow bot commands to also be processed
    #     await self.bot.process_commands(message)

# Add the cog to the bot
def setup(bot):
    bot.add_cog(MessageEvents(bot))
