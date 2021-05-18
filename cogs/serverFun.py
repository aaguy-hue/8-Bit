import discord
import asyncio
from discord.ext import commands

class ServerFun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # @commands.command(aliases=["const"])
    # @commands.cooldown(1, 10800, commands.BucketType.guild)
    # @commands.bot_has_permissions(send_messages=True, mention_everyone=True)
    # async def construct(self, ctx, item: str, *, args=None):
    #     def respond(msg):
    #         return msg.author == ctx.author and msg.channel == ctx.channel
        
    #     item = item.casefold()
    #     if item == "channel":
    #         await ctx.send("Sure, what do you want to call it?")
    #         try:
    #             channelName = await self.bot.wait_for("message", check=respond, timeout=180.0)
    #             channelName = channelName.content
    #         except asyncio.TimeoutError:
    #             await ctx.send("Aaaaannnnndddd there goes your chance to make a channel.")
    #             return
    #         message = await ctx.send(f"*@*everyone do you want a new channel called `{channelName}`? If so, react with ✅.\nYou have 3 hours to vote. If at least half of you vote, then the channel will be constructed.")
    #         await message.add_reaction("✅")
    #         #ON REACTION CHECK IF HALF PEEPS ARE VOTED, AFTER 3 HOURS THEN STOP 
    #     else:
    #         await ctx.send("I can't understand you, talk properly. So far, I'll allow you to construct channels.")
    
    # @commands.command()
    # async def server(self, ctx):
    #     await ctx.send("Scoring Server located at: https://MyQTKMScoringServer.ritm.repl.co")

def setup(bot):
    bot.add_cog(ServerFun(bot))
