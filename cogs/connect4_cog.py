# Code to import from parent directory https://stackoverflow.com/a/11158224
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

#### IMPORTS ####
import discord
import asyncio
from .GameManager import *
from connect4 import connect4
from discord.ext import commands


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
    
    @staticmethod
    def check(player, channel):
        def predicate(message):
            if message.content.strip() == "":
                return False
            try:
                return message.content[0].lower() in ('y', 'n') and message.channel == channel and message.author.id == player.id
            except Exception as e:
                print("wtmoo, u have an error", e)
                return False
        return predicate

    # Commands
    @commands.group(name="c4", aliases=["connect4", "connectFour"], pass_context=True, invoke_without_command=True)
    @commands.bot_has_permissions(send_messages=True, manage_messages=True)
    async def c4(self, ctx, opponent: discord.Member=None):
        ai = False
        if opponent is None or opponent.id == self.bot.user.id:
            await ctx.send("You wanna fight me kiddo? You know I was a champion back in my day 😤. Get ready to LOSE!")
            await asyncio.sleep(1)
            await ctx.send("[LOG] Another person has been hired to manage this game, due to the previous person becoming hyper.")
            ai = True
            opponent = self.bot.user
            await ctx.send("[LOG] Previous person has now actually been fired for accepting the request despite AI not being implemented yet.")
            return
        elif opponent.id == ctx.author.id:
            errorEmbed = discord.Embed(
                title="<:GamilyError:829139949236256790> ERROR",
                description="How desperate are you to win? Go to [this video](https://www.youtube.com/watch?v=srAzlF4VcCA) to find out."
            ).set_footer(
                text="Made by DJ Snowball",
                icon_url=self.bot.icon_url
            )
            await ctx.send(embed=errorEmbed)
            return
        elif opponent.bot:
            errorEmbed = discord.Embed(
                title="<:GamilyError:829139949236256790> ERROR",
                description="🤖 Sorry, you can't play connect 4 with bots other than me.\nPlease see [this video](https://www.youtube.com/watch?v=Hi3GSCwWc54) for more information."
            ).set_footer(
                text="Made by DJ Snowball",
                icon_url=self.bot.icon_url
            )
            await ctx.send(embed=errorEmbed)
            return

        await ctx.send(f"YOU, {opponent.mention} have been challenged to connect four by {ctx.author.mention}. Will you have the courage to face them? (y/n)")
        
        try:
            accepted = await self.bot.wait_for('message', timeout=120, check=self.check(opponent, ctx.channel))
        except asyncio.TimeoutError:
            await ctx.send("Wow, what a noob, they didn't even reply")
            return

        if accepted.content[0].lower() == "n":
            await ctx.send("Sure man")
            return

        rows = 6
        cols = 7
        gameData = {ctx.author.display_name: ctx.author, opponent.display_name: opponent}
        game = connect4.Game(
            rows=rows, 
            columns=cols, 
            player1=ctx.author.display_name, 
            player2=opponent.display_name, 
            data=gameData,
        )
        try:
            self.games.add(game)
        except GameAlreadyExistsError:
            await ctx.send("Sorry, you or your opponent already have an ongoing game! Finish that game first, then you can start another.")
            return
        boardMessage = f"1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣\n{game.generateMessage()}"
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
        
        while self.games.gameExists(game):
            currentPlayer = game.players[game.move_count%2]
            opponentPlayer = game.players[not game.move_count%2]
            # If we're playing against the AI, and it's the AI's turn, we go
            # Else, the player gets to go 
            if ai and game.move_count%2 == 1:
                col = connect4.get_optimal_move(game, isMaximizing=False)
            else:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=self.check_reaction_c4(["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"], currentPlayer.name), timeout=240.0)
                except asyncio.TimeoutError:
                    await ctx.send(f"Oh well I guess {gameData[currentPlayer.name].mention} is just scared.")
                    self.games.endGame(game)
                    return
                if   reaction.emoji == "1️⃣": col = 1
                elif reaction.emoji == "2️⃣": col = 2
                elif reaction.emoji == "3️⃣": col = 3
                elif reaction.emoji == "4️⃣": col = 4
                elif reaction.emoji == "5️⃣": col = 5
                elif reaction.emoji == "6️⃣": col = 6
                elif reaction.emoji == "7️⃣": col = 7
                else:
                    await ctx.send("um...")
                    await ctx.send(f"[ERROR] C4 Reaction Bypassed Check: {reaction.emoji}")
                    self.games.endGame(game)
                    return
            
            if game.add_chip(col-1) == -1:
                errorEmbed = discord.Embed(
                    title="<:GamilyError:829139949236256790> ERROR",
                    description="Sorry, that column is already filled."
                ).set_footer(
                    text="Made by DJ Snowball",
                    icon_url=self.bot.icon_url
                )
                await ctx.send(embed=errorEmbed)
                continue
            for reaction in gameMessage.reactions:
                users = await reaction.users().flatten()
                [await reaction.remove(user) for user in users if not user.id == self.bot.user.id]
            
            result = game.winning_tiles()
            if result:
                # Update the board to show that the player won
                boardMessage = f"1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣\n{game.generateMessage(winning_tiles=result)}"
                embed.remove_field(0)
                embed.add_field(name=f"{currentPlayer.name} wins!", value=boardMessage, inline=False)
                await gameMessage.edit(embed=embed)
                # Send a message that the player won, and break out of the loop.
                await ctx.send(f"Whoaaaaa {gameData[currentPlayer.name].mention} won!")
                self.games.endGame(game)
                return
            elif result == False:
                boardMessage = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣\n" + game.generateMessage()
                embed.remove_field(0)
                embed.add_field(name=f"Tie!", value=boardMessage, inline=False)
                await gameMessage.edit(embed=embed)

                self.games.endGame(game)
                await ctx.send("BRUUUUHHHH. Neither of you won, you somehow managed to fill up the board.")
                return
            elif result is None:
                boardMessage = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣\n" + game.generateMessage()
                embed.remove_field(0)
                embed.add_field(name=f"{opponentPlayer.name}'s turn!", value=boardMessage, inline=False)
                await gameMessage.edit(embed=embed)
        self.games.endGame(game)
        await ctx.send("How did you- somehow you broke the game.")

    @c4.command(name="ai", aliases=["bot", "singleplayer", "oneplayer", "single", "one"], pass_context=True, invoke_without_command=True)
    @commands.bot_has_permissions(send_messages=True, manage_messages=True)
    async def ai(self, ctx):
        await ctx.send("This command is not implemented yet.")
        return
        # await ctx.invoke(self.bot.get_command('c4'), opponent=self.bot.user)
    
    @c4.command(name="endGame", aliases=["end", "quit", "resign", "stop"], pass_context=True, invoke_without_command=True)
    @commands.bot_has_permissions(send_messages=True)
    async def endGame(self, ctx):
        await ctx.send("k")
        game = self.games.getGame(ctx.author)
        if game is None:
            errorEmbed = discord.Embed(
                title="<:GamilyError:829139949236256790> ERROR",
                description="You're not in any games. For information on joining games, refer to [this video](https://www.youtube.com/watch?v=RkzhZsf4Dro)"
            ).set_footer(
                text="Made by DJ Snowball",
                icon_url=self.bot.icon_url
            )
            await ctx.send(embed=errorEmbed)
            return
        self.games.endGame(game)
        await ctx.send("The game has ended.")
    
    @c4.command(name="predict", pass_context=True, invoke_without_command=True)
    @commands.bot_has_permissions(send_messages=True)
    async def predict(self, ctx):
        game = self.games.getGame(ctx.author)
        if game is None:
            errorEmbed = discord.Embed(
                title="<:GamilyError:829139949236256790> ERROR",
                description="You're not in any games. For information on joining games, refer to [this video](https://www.youtube.com/watch?v=RkzhZsf4Dro)"
            )
            await ctx.send(embed=errorEmbed)
            return
        
        await ctx.send("Whoops, this isn't implemented yet. Once AI is implemented, I'll add very similar logic in order to predict the winner.")
        # await ctx.send("Okay, lemme think")
        # winner = connect4.predict_winner(game, game.move_count%2)
        # await ctx.send(f"{list(game.data.values())[winner]} is the most likely to win the game!")

def setup(bot):
    bot.add_cog(Connect4(bot))
