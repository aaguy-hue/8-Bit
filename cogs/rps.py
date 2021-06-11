"""RPS, aka rock paper scissors. Made by Shuban!!!"""

import random
import discord
import asyncio
from discord.ext import commands
import discord_components

class RockPaperScissors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Play with .rps [your choice]", aliases=['rps'])
    async def rockpaperscissors(self, ctx, user_choice=None):
        rpsGame = ['rock', 'paper', 'scissors']

        if not user_choice:
            embed = discord.Embed(
                title="Rock, Paper, Scissors", 
                description="Choose now or else I'll steal all your legos and delete your Minecraft account..."
            ).set_footer(
                text=f"Made by {self.bot.contributors['HYPERION']}",
                icon_url=self.bot.icon_url
            )

            components = [
                discord_components.Button(
                    label="Rock",
                    emoji="🪨",
                    style=4
                ),
                discord_components.Button(
                    label="Paper",
                    emoji="📰",
                    style=1
                ),
                discord_components.Button(
                    label="Scissors",
                    emoji="✂",
                    style=3
                ),
            ]
            message = await ctx.send(
                embed=embed,
                components=[
                    components
                    # discord_components.Select(
                    #     placeholder="Select an option...",
                    #     options=[
                    #         discord_components.Option(
                    #             label="Rock",
                    #             value="rock"
                    #         ),
                    #         discord_components.Option(
                    #             label="Paper",
                    #             value="paper",
                    #             emoji="📰"
                    #         ),
                    #         discord_components.Option(
                    #             label="Scissors",
                    #             value="scissors",
                    #             emoji="✂"
                    #         )
                    #     ]
                    # ),
                ]
            )

            def check(i):
                return i.component.label.lower() in rpsGame and i.user == ctx.author and i.message.id == message.id

            try:
                interaction = await self.bot.wait_for("button_click", check=check)
                for component in range(3):
                    components[component].disabled = True
                
                await message.edit(components=[components])
                await interaction.respond(content="Got it! Now let's wait for the AI to make its move!")
            except asyncio.TimeoutError:
                await ctx.send("Are you even there? I'm just ending this ***sigh***.")
                return
            user_choice = interaction.component.label.lower()
        else:
            user_choice = user_choice.lower()
            if not (user_choice in rpsGame):
                await ctx.send("That's not a valid choice!")
                return

        comp_choice = random.choice(rpsGame)
        if user_choice == 'rock':
            if comp_choice == 'rock':
                await ctx.send(f'Lel. We tied. It do be like that sometimes though.\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(f'HA I won! You owe me a sprite!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(f"Bruh I have never won in my life let me win at least once. 🥲 Anyway.\nYour choice: {user_choice}\nMy choice: {comp_choice}")

        elif user_choice == 'paper':
            if comp_choice == 'rock':
                await ctx.send(f'If only a rock was shot at a paper that was held with two clips and had nothing behind it. Welp I guess it cant always be like that so gg.\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(f'Bruh. We just tied. I\'ll probably beat you next time though \nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(f"Bippity boppity this win is now my property.\nYour choice: {user_choice}\nMy choice: {comp_choice}")

        elif user_choice == 'scissors':
            if comp_choice == 'rock':
                await ctx.send(f'LOL imagine using scissors to cut a rock.\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'paper':
                await ctx.send(f'MASAKA, you just used your secret move!\nYour choice: {user_choice}\nMy choice: {comp_choice}')
            elif comp_choice == 'scissors':
                await ctx.send(f"We just tied but I know I won so lol 😏.\nYour choice: {user_choice}\nMy choice: {comp_choice}")
        

def setup(bot):
    bot.add_cog(RockPaperScissors(bot))