import discord
import discord_components
from discord.ext import commands

class Minecraft2d(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def minecraft(self, ctx, seed=None):
        pass
    
def setup(bot):
    return

    bot.add_cog(Minecraft2d(bot))
