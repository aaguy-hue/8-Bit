import discord
import os
import json
import asyncio
import datetime
from discord.ext import commands
from dotenv import load_dotenv
from connect4 import connect4 as connect4

load_dotenv()

# Store constants
PREFIX = r"g "
TOKEN = os.getenv("TOKEN")
# Store variables
games = []

# Helper Functions
def check_reaction_c4(emojis, player):
    def predicate(reaction, user):
        return str(reaction.emoji) in emojis and user.display_name==player
    return predicate

# The bot
bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or(PREFIX))

@bot.event
async def on_ready():
    print("heyyyy I'm back")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.CommandOnCooldown):
        hours, minutes, seconds = str(datetime.timedelta(seconds=round(error.retry_after))).split(":")
        timeLeft = f"{hours} hours, {minutes} minutes, and {seconds} seconds"
        await ctx.send(f"The people of QZ can construct another item in {timeLeft}.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"You didn't specify the `{error.param.name}` argument.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("You didn't give a valid arugment.")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("Yeah I don't think you're allowed to do that buddy.")
    elif isinstance(error, commands.MissingPermissions):
        missing_perms = ', '.join(error.missing_perms)
        await ctx.send(f"You're missing the following permissions: {missing_perms}")
    elif isinstance(error, commands.RoleNotFound):
        await ctx.send("Uh kid that role doesn't exist in this server")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("Whoa what's up with the wall of text? Stop giving me so many arugments!")
    elif isinstance(error, commands.UnexpectedQuoteError):
        await ctx.send("Sorry kiddo you gotta use the quotes to wrap the whole argument")
    elif isinstance(error, commands.UserNotFound):
        await ctx.send("I'm sorry but that user isn't in this server")
    elif isinstance(error, commands.PrivateMessageOnly):
        await ctx.send("You can only use this command in DMs")
    elif isinstance(error, commands.UserInputError):
        # this should never occur since UnexpectedQuoteError, MissingRequiredArgument, and BadArgument are there
        await ctx.send("Uh what did you say?")
    elif isinstance(error, commands.MissingRole):
        await ctx.send(f"You need `{error.missing_role.name}` in order to use this command")
    elif isinstance(error, commands.BotMissingRole):
        await ctx.send(f"I need the `{error.missing_role.name}` role in order to run this command")
    elif isinstance(error, commands.errors.BotMissingPermissions):
        missing_perms = ', '.join(error.missing_perms)
        await ctx.send(f"I need the following permissions to run this command: `{missing_perms}`")
    else:
        raise error

@bot.event
async def on_message(message):
    # Process the commands
    await bot.process_commands(message)

@bot.command(aliases=["connect4", "connectFour"])
async def c4(ctx, opponent: discord.Member):
    if opponent.id == ctx.author.id:
        await ctx.send("How desperate are you to win?")
        return

    rows = 6
    cols = 7
    gameData = {ctx.author.display_name: ctx.author, opponent.display_name: opponent}
    game = connect4.Game(rows=rows, columns=cols, player1=ctx.author.display_name, player2=opponent.display_name, data=gameData)
    boardMessage = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣\n" + game.generateMessageInverse()
    embed = discord.Embed(title="Connect Four", description=f"🔴 {ctx.author.display_name} | 🟡 {opponent.display_name}")
    embed.add_field(name=f"{ctx.author.display_name}'s turn!", value=boardMessage, inline=False)
    gameMessage = await ctx.send(embed=embed)
    gameMessage = discord.utils.get(bot.cached_messages, id=gameMessage.id)
    
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
            reaction, user = await bot.wait_for('reaction_add', check=check_reaction_c4(["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"], currentPlayer.name), timeout=120.0)
        except asyncio.TimeoutError:
            await ctx.send(f"Oh well I guess {gameData[currentPlayer.name].mention} is just scared.")
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
                return
            
            if game.add_chip(col-1) == -1:
                await ctx.send("very bad, that column is already filled, FOOL")
                continue
            for reaction in gameMessage.reactions:
                users = await reaction.users().flatten()
                [await reaction.remove(user) for user in users if not user.id == bot.user.id]
            
            if game.check_player_wins():
                # Update the board to show that the player won
                boardMessage = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣\n" + game.generateMessageInverse()
                embed.remove_field(0)
                embed.add_field(name=f"{currentPlayer.name} wins!", value=boardMessage, inline=False)
                await gameMessage.edit(embed=embed)
                # Send a message that the player won, and break out of the loop.
                await ctx.send(f"Whoaaaaa {gameData[currentPlayer.name].mention} won!")
                gameIsGoing = False
                break
            
            boardMessage = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣\n" + game.generateMessageInverse()
            embed.remove_field(0)
            embed.add_field(name=f"{opponentPlayer.name}'s turn!", value=boardMessage, inline=False)
            await gameMessage.edit(embed=embed)

@bot.command(aliases=["const"])
@commands.cooldown(1, 10800, commands.BucketType.guild)
async def construct(ctx, item: str, *, args=None):
    def respond(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    item = item.casefold()
    if item == "channel":
        await ctx.send("Sure, what do you want to call it?")
        try:
            channelName = await bot.wait_for("message", check=respond, timeout=180.0)
            channelName = channelName.content
        except asyncio.TimeoutError:
            await ctx.send("Aaaaannnnndddd there goes your chance to make a channel.")
            return
        message = await ctx.send(f"*@*everyone do you want a new channel called `{channelName}`? If so, react with ✅.\nYou have 3 hours to vote. If at least half of you vote, then the channel will be constructed.")
        await message.add_reaction("✅")
        #ON REACTION CHECK IF HALF PEEPS ARE VOTED, AFTER 3 HOURS THEN STOP 
    else:
        await ctx.send("I can't understand you, talk properly. So far, I'll allow you to construct channels.")

@bot.command()
async def server(ctx):
    await ctx.send("Scoring Server located at: https://MyQTKMScoringServer.ritm.repl.co")

bot.run(TOKEN)
