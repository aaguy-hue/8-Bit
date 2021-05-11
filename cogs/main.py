import asyncio
import discord
import json
import itertools
from discord.ext import commands

class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("command_list.json", "r") as f:
            self.bot_commands = json.load(f)
    
    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def help(self, ctx, command: str = None):
        # Mostly copied from my other bot, CyberTools https://github.com/aaguy-hue/CyberToolsBot

        if command is None:
            embed = discord.Embed(
                title="Help",
                description=f"**PREFIX: {ctx.prefix}**\nUse `{ctx.prefix}help <command>` for more information on a command.",
                color=ctx.author.color
            )
            for group in self.bot_commands:
                groupcmds = ' '.join((f"`{x['name']}`" for x in group["commands"]))
                embed.add_field(name=group["group"], value=groupcmds)
        else:
            info = list(itertools.chain(*(list(filter(lambda x: (x['command'] == command) or (command in x['aliases']), group["commands"])) for group in self.bot_commands)))
            print(info)
            if (len(info) > 1):
                await ctx.send(f"It seems that there are multiple commands with that name. Please report it in our (support server)[{self.bot.support_server}]")
                return
            elif (len(info) < 1):
                await ctx.send(f"The command \"{command}\" wasn't found. Make sure you typed it in correctly, and retry.")
                return
            info = info[0]
            syntax = f"{ctx.prefix}{info['syntax']}"
            arguments = info['arguments']
            description = info['description']
            if (info['aliases'] == [None]):
                aliases = None
            else:
                aliases = ', '.join(info['aliases'])
            embed = discord.Embed(
                title=info['command'],
                description=f"**SYNTAX**: {syntax}\n**ALIASES**: {aliases}\n\n{arguments}\n{description}",
                color=ctx.author.color
            )
        embed.add_field(
            name="Links",
            value=f"[Invite Me]({self.bot.invite_link}) - [Support Server]({self.bot.support_server})",
            inline=False
        )
        embed.set_footer(text="Made by DJ Snowball", icon_url=f"{self.bot.icon_url}")
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["inv"])
    @commands.bot_has_permissions(send_messages=True)
    async def invite(self, ctx):
        await ctx.send(
            f"If you want to invite the bot to your server, you can use this link -> {self.bot.invite_link}"
        )
    
    @commands.command(aliases=["botstat", "botstats"])
    @commands.bot_has_permissions(send_messages=True)
    async def botinfo(self, ctx):
        servercount = f"I'm in {len(self.bot.guilds)} servers!\nIf you want to increase this number, run `{ctx.prefix}invite` and press the link to invite me to more servers!"

        embed = discord.Embed(title="Bot Statistics")
        embed.add_field(name="Server Count", value=servercount, inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Main(bot))
