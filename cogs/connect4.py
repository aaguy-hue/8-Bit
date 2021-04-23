# Code to import from parent directory https://stackoverflow.com/a/11158224
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

#### IMPORTS ####
import discord
import asyncio
from discord.ext import commands
from connect4 import connect4

class GameAlreadyExistsError(Exception): pass
class NotAGameError(Exception): pass

# https://stackoverflow.com/a/41281734
class GameManager(set):
    def add(self, value):
        if not isinstance(value, connect4.Game):
            raise NotAGameError('Value {!r} is not a game'.format(value))
            return
        # https://stackoverflow.com/a/17735466
        if value in self or [True for other in self if not set(value.data.values()).isdisjoint(other.data.values())]:
            raise GameAlreadyExistsError('Game {!r} already exists'.format(value))
            return
        super().add(value)

    def update(self, values):
        for value in values:
            if value in self:
                raise GameAlreadyExistsError('Game {!r} already exists'.format(error_values))
            if not isinstance(value, connect4.Game):
                raise NotAGameError('Value {!r} is not a game'.format(value))
        super().update(values)
    
    def endGame(self, game):
        self.remove(game)
    
    def getGame(self, player1):
        for game in self:
            if player1 in game.data.values():
                return game


class Connect4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = GameManager()
    
    # Helper Functions
    @staticmethod
    def check_reaction_c4(emojis, player):
        def predicate(reaction, user):
            return str(reaction.emoji) in emojis and user.display_name==player
        return predicate

    @commands.group(name="c4", aliases=["connect4", "connectFour"], pass_context=True, invoke_without_command=True)
    async def c4(self, ctx, opponent: discord.Member):
        if opponent.id == ctx.author.id:
            errorEmbed = discord.Embed(
                title="<:GamilyError:829139949236256790> ERROR",
                description="How desperate are you to win? Go to [this video](https://www.youtube.com/watch?v=srAzlF4VcCA) to find out."
            )
            await ctx.send(embed=errorEmbed)
            return
        if opponent.bot:
            errorEmbed = discord.Embed(
                title="<:GamilyError:829139949236256790> ERROR",
                description="🤖 Sorry, you can't play connect 4 with bots other than me.\nPlease see [this video](https://www.youtube.com/watch?v=Hi3GSCwWc54) for more information."
            )
            await ctx.send(embed=errorEmbed)
            return

        rows = 6
        cols = 7
        gameData = {ctx.author.display_name: ctx.author, opponent.display_name: opponent}
        game = connect4.Game(rows=rows, columns=cols, player1=ctx.author.display_name, player2=opponent.display_name, data=gameData)
        try:
            self.games.add(game)
        except GameAlreadyExistsError:
            await ctx.send("Sorry, you already have an ongoing game! Finish that game first, then you can make another.")
            return
        boardMessage = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣\n" + game.generateMessageInverse()
        embed = discord.Embed(title="Connect Four", description=f"🔴 {ctx.author.display_name} | 🟡 {opponent.display_name}")
        embed.add_field(name=f"{ctx.author.display_name}'s turn!", value=boardMessage, inline=False)
        gameMessage = await ctx.send(embed=embed)
        gameMessage = discord.utils.get(self.bot.cached_messages, id=gameMessage.id)
        
        await gameMessage.add_reaction("1️⃣")
        await gameMessage.add_reaction("2️⃣")
        await gameMessage.add_reaction("3️⃣")
        await gameMessage.add_reaction("4️⃣")
        await gameMessage.add_reaction("5️⃣")
        await gameMessage.add_reaction("6️⃣")
        await gameMessage.add_reaction("7️⃣")
        
        gameIsGoing = True
        while gameIsGoing:
            currentPlayer = game.players[game.move_count%2]
            opponentPlayer = game.players[~game.move_count%2]
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=self.check_reaction_c4(["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"], currentPlayer.name), timeout=120.0)
            except asyncio.TimeoutError:
                await ctx.send(f"Oh well I guess {gameData[currentPlayer.name].mention} is just scared.")
                self.games.endGame(game)
                return
            else:
                if reaction.emoji == "1️⃣":
                    col = 1
                elif reaction.emoji == "2️⃣":
                    col = 2
                elif reaction.emoji == "3️⃣":
                    col = 3
                elif reaction.emoji == "4️⃣":
                    col = 4
                elif reaction.emoji == "5️⃣":
                    col = 5
                elif reaction.emoji == "6️⃣":
                    col = 6
                elif reaction.emoji == "7️⃣":
                    col = 7
                else:
                    await ctx.send("um...")
                    print(f"[ERROR] C4 Reaction Bypassed Check: {reaction.emoji}")
                    self.games.endGame(game)
                    return
                
                if game.add_chip(col-1) == -1:
                    errorEmbed = discord.Embed(
                        title="<:GamilyError:829139949236256790> ERROR",
                        description="Sorry, that column is already filled."
                    )
                    await ctx.send(embed=errorEmbed)
                    continue
                for reaction in gameMessage.reactions:
                    users = await reaction.users().flatten()
                    [await reaction.remove(user) for user in users if not user.id == self.bot.user.id]
                
                if game.check_player_wins():
                    # Update the board to show that the player won
                    boardMessage = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣\n" + game.generateMessageInverse()
                    embed.remove_field(0)
                    embed.add_field(name=f"{currentPlayer.name} wins!", value=boardMessage, inline=False)
                    await gameMessage.edit(embed=embed)
                    # Send a message that the player won, and break out of the loop.
                    await ctx.send(f"Whoaaaaa {gameData[currentPlayer.name].mention} won!")
                    self.games.endGame(game)
                    return
                
                boardMessage = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣\n" + game.generateMessageInverse()
                embed.remove_field(0)
                embed.add_field(name=f"{opponentPlayer.name}'s turn!", value=boardMessage, inline=False)
                await gameMessage.edit(embed=embed)
        self.games.endGame(game)
        await ctx.send("How did you-")

    @c4.command(name="endGame", aliases=["end", "quit"], pass_context=True, invoke_without_command=True)
    async def endGame(self, ctx):
        await ctx.send("k")
        print(self.games.endGame((self.games.getGame(ctx.author))))
        await ctx.send("The game has ended.")

def setup(bot):
    bot.add_cog(Connect4(bot))
