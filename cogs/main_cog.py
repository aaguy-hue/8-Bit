import os
import json
import discord
import itertools
from discord.ext import commands

class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/command_list.json"), "r") as f:
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
            ).set_footer(
                text="Made by DJ Snowball",
                icon_url=self.bot.icon_url
            )
            for group in self.bot_commands:
                groupcmds = ' '.join((f"`{x['name']}`" for x in group["commands"]))
                embed.add_field(name=group["group"], value=groupcmds)
        else:
            info = list(itertools.chain(*(list(filter(lambda x: (x['command'] == command) or (command in x['aliases']), group["commands"])) for group in self.bot_commands)))
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
            ).add_field(
                name="Links",
                value=f"[Invite Me]({self.bot.invite_link}) - [Support Server]({self.bot.support_server}) - [Vote for Me]({self.bot.voting_url})",
                inline=False
            )
        embed.set_footer(text="Made by DJ Snowball", icon_url=f"{self.bot.icon_url}")
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["inv", "support"])
    @commands.bot_has_permissions(send_messages=True)
    async def invite(self, ctx):
        embed = discord.Embed(
            title="Invites", 
            description="The links to invite the bot and join the support server."
        ).add_field(
            name="Bot Invite", 
            value=self.bot.invite_link
        ).add_field(
            name="Support Server", 
            value=self.bot.support_server
        ).set_footer(
            text="Made by DJ Snowball",
            icon_url=self.bot.icon_url
        )
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["botstat", "botstats"])
    @commands.bot_has_permissions(send_messages=True)
    async def botinfo(self, ctx):
        servercount = f"I'm in {len(self.bot.guilds)} servers!\nIf you want to increase this number, run `{ctx.prefix}invite` and press the link to invite me to more servers!"
        changelog = " - Tic Tac Toe has been added!\n - A rewrite of the connect four game behind the scenes to make it much faster and to allow to add AI"
        comingsoon = " - Tic Tac Toe AI\n - Minecraft Clone"

        embed = discord.Embed(
            title="Bot Statistics"
        ).add_field(
            name="Server Count", 
            value=servercount, 
            inline=False
        ).add_field(
            name="Changelog",
            value=changelog,
            inline=True
        ).add_field(
            name="Coming Soon",
            value=comingsoon,
            inline=True
        ).set_footer(
            text="Made by DJ Snowball",
            icon_url=self.bot.icon_url
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def vote(self, ctx):
        embed = discord.Embed(
            title="Vote", 
            description=self.bot.voting_url
        ).set_footer(
            text="Made by DJ Snowball",
            icon_url=self.bot.icon_url
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    async def prefix(self, ctx, prefix=None):
        if prefix is None:
            await ctx.send(f"My prefix is `{(await self.bot.get_prefix_(self.bot, ctx.message))[-1]}`!")
        else:
            await ctx.send(f"Unfortunately, setting the prefix has been disabled due to technical difficulties. Join the support server for more info <{self.bot.support_server}>")
            # if not ctx.author.guild_permissions.manage_guild:
            #     await ctx.send("You must have the \"Manage Server\" permission to change the server prefix. If you meant to get the prefix, don't pass in any arguments.")
            #     return
            
            # with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/prefixes.json"), "r+") as f:
            #     file_data = json.load(f)
            #     file_data.update({str(ctx.guild.id): prefix})
            #     f.seek(0)
            #     print(file_data)
            #     # convert back to json.
            #     f.write(json.dumps(file_data))
            
            # await ctx.send(f"The prefix has successfully been changed to `{prefix}`!")


def setup(bot):
    bot.add_cog(Main(bot))
