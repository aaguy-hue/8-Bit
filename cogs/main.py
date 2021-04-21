import asyncio
import discord
from discord.ext import commands

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["inv"])
    async def invite(self, ctx):
        await ctx.send(
            "If you want to invite the bot to your server, you can use this link -> https://discord.com/api/oauth2/authorize?client_id=705890912282345472&permissions=511040&scope=bot"
        )


def setup(bot):
    bot.add_cog(Main(bot))
