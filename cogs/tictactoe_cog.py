# Code to import from parent directory https://stackoverflow.com/a/11158224
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

##### IMPORTS #####
import random
import asyncio
import discord
from tools import imageapi
from .GameManager import *
from tictactoe import tictactoe
from discord.ext import commands

# My savior: https://stackoverflow.com/a/61579108
class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = GameManager()
    
    # Helper Functions
    @staticmethod
    def check_reaction(emojis, player):
        def predicate(reaction, user):
            return str(reaction.emoji) in emojis and user.display_name==player
        return predicate
    
    @staticmethod
    def check(player, channel):
        def predicate(message):
            return message.content[0].lower() in ('y', 'n') and message.channel == channel and message.author.id == player.id
        return predicate
    
    # Commands
    @commands.group(name="tictactoe", aliases=["TicTacToe"], pass_context=True, invoke_without_command=True)
    @commands.bot_has_permissions(send_messages=True, manage_messages=True)
    async def tictactoe(self, ctx, opponent: discord.Member):        
        if ctx.author.id == opponent.id:
            await ctx.send("🤦‍♂️")
            return
        await ctx.send(f"YOU, {opponent.mention} have been challenged to tic tac toe by {ctx.author.mention}. Will you have the courage to face them? (y/n)")
        
        try:
            accepted = await self.bot.wait_for('message', timeout=120, check=self.check(opponent, ctx.channel))
        except asyncio.TimeoutError:
            await ctx.send("Wow, what a noob, they didn't even reply")
            return

        if accepted.content[0].lower() == "n":
            await ctx.send("Sure man")
            return

        playersdict = {ctx.author.display_name: ctx.author, opponent.display_name: opponent}
        playerkeys = random.sample([ctx.author.display_name, opponent.display_name], 2)
        players = {k: playersdict[k] for k in playerkeys}

        game = tictactoe.Game(p1=playerkeys[0], p2=playerkeys[1], data=players)
        try:
            self.games.add(game)
        except GameAlreadyExistsError:
            await ctx.send("Hey, it seems like either you or your opponent are already in a game. Finish that first, then you can do this.")
            return
        
        
        image = imageapi.PILupload(game.generate_image())
        embed = discord.Embed(
            title="Tic Tac Toe",
            description=f"❌ {playerkeys[0]} | ⭕ {playerkeys[1]}"
        ).add_field(
            name=f"{playerkeys[0]}'s turn!",
            value="** **",
            inline=False
        ).set_image(url=image['data']['link'])
        gameMessage = await ctx.send(embed=embed)
        gameMessage = discord.utils.get(self.bot.cached_messages, id=gameMessage.id)

        #region reactions
        await gameMessage.add_reaction("1️⃣")
        await gameMessage.add_reaction("2️⃣")
        await gameMessage.add_reaction("3️⃣")
        await gameMessage.add_reaction("4️⃣")
        await gameMessage.add_reaction("5️⃣")
        await gameMessage.add_reaction("6️⃣")
        await gameMessage.add_reaction("7️⃣")
        await gameMessage.add_reaction("8️⃣")
        await gameMessage.add_reaction("9️⃣")
        #endregion

        while self.games.gameExists(game):
            currentPlayer = playerkeys[game.move_count%2]
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=self.check_reaction(["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"], currentPlayer), timeout=240.0)
            except asyncio.TimeoutError:
                await ctx.send(f"b r u h")
                self.games.endGame(game)
                return
            if   reaction.emoji == "1️⃣": index = 1
            elif reaction.emoji == "2️⃣": index = 2
            elif reaction.emoji == "3️⃣": index = 3
            elif reaction.emoji == "4️⃣": index = 4
            elif reaction.emoji == "5️⃣": index = 5
            elif reaction.emoji == "6️⃣": index = 6
            elif reaction.emoji == "7️⃣": index = 7
            elif reaction.emoji == "8️⃣": index = 8
            elif reaction.emoji == "9️⃣": index = 9
            else:
                await ctx.send("um...")
                await ctx.send(f"[ERROR] Reaction Bypassed Check: {reaction.emoji}")
                self.games.endGame(game)
                return
            
            # If it was a valid move, continue, else wait again
            if game.make_move_index(index):

                await reaction.clear()
                
                results = game.game_results()
                
                image = imageapi.PILupload(game.generate_image(results))
                embed.add_field(
                    name=f"{playerkeys[game.move_count%2]}'s turn!",
                    value="** **",
                    inline=False
                ).set_image(url=image['data']['link']).remove_field(0)
                await gameMessage.edit(embed=embed)

                if results:
                    await ctx.send(f"🎉 {players[currentPlayer].mention} wins!")
                elif results == False:
                    await ctx.send(f"🤔 You guys tied, but I can't tell if you guys both suck or you're both decent.")

def setup(bot):
    bot.add_cog(TicTacToe(bot))