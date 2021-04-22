import asyncio
import discord
from discord.ext import commands

class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(aliases=["inv"])
    async def invite(self, ctx):
        await ctx.send(
            "If you want to invite the bot to your server, you can use this link -> https://discord.com/api/oauth2/authorize?client_id=705890912282345472&permissions=511040&scope=bot"
        )
    
    @commands.command(aliases=["botstat", "botstats"])
    async def botinfo(self, ctx):
        servercount = f"I'm in {len(self.bot.guilds)} servers!\nIf you want to increase this number, run `g invite` and press the link to invite me to more servers!"

        embed = discord.Embed(title="Bot Statistics")
        embed.add_field(name="Server Count", value=servercount, inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Main(bot))
