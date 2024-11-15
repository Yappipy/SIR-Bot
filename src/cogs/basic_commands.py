import discord

from discord.ext import commands



class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.author.name}!')

    @commands.slash_command(name='hello')
    async def slash_hello(self, ctx: discord.ApplicationContext):
        await ctx.respond(f'Hello, {ctx.author.name}!')

    @commands.command(name="Emir")
    async def Emir(self, ctx):
        await ctx.send("Lol, you gae asf Emir")

    @commands.command(name="chocolatine")
    async def Emir(self, ctx):
        await ctx.send("You meant Hybe ? He dumbo ")

    
# Add the cog to the bot
def setup(bot):
    bot.add_cog(BasicCommands(bot))
