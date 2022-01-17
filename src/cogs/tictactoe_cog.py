"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

# Code to import from parent directory https://stackoverflow.com/a/11158224
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

##### IMPORTS #####
import random
import asyncio
import discord
import discord_components
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
        
    # Commands
    @commands.group(name="tictactoe", aliases=["TicTacToe", "ttt"], pass_context=True, invoke_without_command=True)
    @commands.bot_has_permissions(send_messages=True, manage_messages=True)
    async def ttt(self, ctx, opponent: discord.Member=None):
        EMOJI_TO_INT = {
            "1️⃣": 1,
            "2️⃣": 2,
            "3️⃣": 3,
            "4️⃣": 4,
            "5️⃣": 5,
            "6️⃣": 6,
            "7️⃣": 7,
            "8️⃣": 8,
            "9️⃣": 9,
        }
        INT_TO_EMOJI = {
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣",
            6: "6️⃣",
            7: "7️⃣",
            8: "8️⃣",
            9: "9️⃣",
        }

        ai = False
        if opponent is None or opponent.id == self.bot.user.id:
            # await ctx.send("I don't even know how to play tic tac toe, let alone be a worthy AI.")
            # return
            
            ai = True
            opponent = self.bot.user
            await ctx.send("Wow, you actually dare challenge me? So be it.")
        elif ctx.author.id == opponent.id:
            await ctx.send("🤦‍♂️ You can't play against yourself.")
            return
        elif opponent.bot:
            await ctx.send("You can try to compete against robots, but don't expect a response 🤷‍♂️.")
            return

        if not ai:
            components = [
                discord_components.Button(
                    label="Yes",
                    style=3
                ),
                discord_components.Button(
                    label="No",
                    style=4
                )
            ]

            message = await ctx.send(
                f"YOU, {opponent.mention} have been challenged to tic tac toe by {ctx.author.mention}. Will you have the courage to face them?",
                components=[components]
            )

            def check(i):
                return i.component.label.lower() in ['yes', 'no'] and i.user.id == opponent.id and i.message.id == message.id

            try:
                interaction = await self.bot.wait_for("button_click", check=check, timeout=120.0)
                components[0].disabled = True
                components[1].disabled = True
                
                await message.edit(components=[components])

                if interaction.component.label.lower() == "no":
                    await interaction.respond(content="Sure", ephemeral=False)
                    return
                await interaction.respond(content="Let the game begin!", ephemeral=False)
            except asyncio.TimeoutError:
                await ctx.send("Wow, what a noob, they didn't even reply")
                return
            
        
        playersdict = {ctx.author.display_name: ctx.author, opponent.display_name: opponent}
        playerkeys = random.sample([ctx.author.display_name, opponent.display_name], 2)
        players = {k: playersdict[k] for k in playerkeys}

        if ai:
            aiplayer = playerkeys.index(self.bot.user.display_name)+1
            humanplayer = playerkeys.index(ctx.author.display_name)+1
        
        game = tictactoe.Game(p1=playerkeys[0], p2=playerkeys[1], data=players)
        try:
            self.games.add(game)
        except GameAlreadyExistsError:
            if not ai:
                await ctx.send("Hey, it seems like either you or your opponent are already in a game. Finish that first, then you can do this.")
                return
        
        
        image_url = game.generate_image()
        embed = discord.Embed(
            title="Tic Tac Toe",
            description=f"❌ {playerkeys[0]} | ⭕ {playerkeys[1]}"
        ).add_field(
            name=f"{playerkeys[0]}'s turn!",
            value="** **",
            inline=False
        ).set_image(
            url=image_url
        ).set_footer(
            text="Made by DJ Snowball",
            icon_url=self.bot.icon_url
        )
        gameMessage = await ctx.send("Tic tac toe AI has been released! Run `g ttt ai` to try it out!", embed=embed)
        gameMessage = discord.utils.get(self.bot.cached_messages, id=gameMessage.id)

        try:
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
        except AttributeError as e:
            await ctx.send(f"Sorry, it seems like I'm not able to add the reaction to the message, please report this to the dev in the support server at {self.bot.support_server}\n```{e}```")

        while self.games.gameExists(game):
            currentPlayer = playerkeys[game.move_count%2]
            ai_turn = players[currentPlayer].id == self.bot.user.id and ai

            if ai_turn:
                index = await game.best_move(aiplayer, humanplayer)
            else:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=self.check_reaction(["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"], currentPlayer), timeout=240.0)
                except asyncio.TimeoutError:
                    await ctx.send(f"oof, they're gone 😢")
                    self.games.endGame(game)
                    return
                
                index = EMOJI_TO_INT[reaction.emoji]
                        
            # If it was a valid move, continue, else wait again
            if game.make_move_index(index):
                
                if not ai_turn:
                    await reaction.clear()
                else:
                    for reaction in gameMessage.reactions:
                        if reaction.emoji == INT_TO_EMOJI[index]:
                            await reaction.clear()
                
                results = game.game_results()
                
                image_url = game.generate_image(results)

                if results:
                    embed.add_field(
                        name=f"{playerkeys[not game.move_count%2]} wins!",
                        value="** **",
                        inline=False
                    ).set_image(url=image_url).remove_field(0)
                    await gameMessage.edit(embed=embed)

                    self.games.endGame(game)
                    await ctx.send(f"🎉 {players[currentPlayer].mention} wins!")
                elif results == False:
                    embed.add_field(
                        name=f"🐈Tie!",
                        value="** **",
                        inline=False
                    ).set_image(url=image_url).remove_field(0)
                    await gameMessage.edit(embed=embed)

                    self.games.endGame(game)
                    await ctx.send(f"🤔 You guys tied, but I can't tell if you guys both suck or you're both decent.")
                else:
                    embed.add_field(
                        name=f"{playerkeys[game.move_count%2]}'s turn!",
                        value="** **",
                        inline=False
                    ).set_image(url=image_url).remove_field(0)
                    await gameMessage.edit(embed=embed)
    
    @ttt.command(name="ai", aliases=["bot", "singleplayer", "oneplayer", "single", "one"], pass_context=True, invoke_without_command=True)
    @commands.bot_has_permissions(send_messages=True, manage_messages=True)
    async def ai(self, ctx):
        await ctx.invoke(self.bot.get_command('ttt'), opponent=self.bot.user)
    
    @ttt.command(name="endGame", aliases=["end", "quit", "resign", "stop"], pass_context=True, invoke_without_command=True)
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

def setup(bot):
    bot.add_cog(TicTacToe(bot))
