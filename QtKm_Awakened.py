"""Using SourSpoon discord.py template"""
import asyncio
import datetime
import json
import logging
from pathlib import Path

import discord
from discord.ext import commands


def config_load():
    with open('data/config.json', 'r', encoding='utf-8') as doc:
        #  Please make sure encoding is correct, especially after editing the config file
        return json.load(doc)


async def run():
    """
    Where the bot gets started. If you wanted to create an database connection pool or other session for the bot to use,
    it's recommended that you create it here and pass it to the bot as a kwarg.
    """

    config = config_load()
    bot = Bot(config=config,
              description=config['description'])
    try:
        await bot.start(config['token'])
    except KeyboardInterrupt:
        await bot.logout()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=self.get_prefix_,
            description=kwargs.pop('description')
        )
        self.start_time = None
        self.app_info = None

        self.loop.create_task(self.track_start())
        self.loop.create_task(self.load_all_extensions())

    async def track_start(self):
        """
        Waits for the bot to connect to discord and then records the time.
        Can be used to work out uptime.
        """
        await self.wait_until_ready()
        self.start_time = datetime.datetime.utcnow()

    async def get_prefix_(self, bot, message):
        """
        A coroutine that returns a prefix.
        I have made this a coroutine just to show that it can be done. If you needed async logic in here it can be done.
        A good example of async logic would be retrieving a prefix from a database.
        """
        prefix = ['g ']
        return commands.when_mentioned_or(*prefix)(bot, message)

    async def load_all_extensions(self):
        """
        Attempts to load all .py files in /cogs/ as cog extensions
        """
        await self.wait_until_ready()
        await asyncio.sleep(1)  # ensure that on_ready has completed and finished printing
        cogs = [x.stem for x in Path('cogs').glob('*.py')]
        for extension in cogs:
            try:
                self.load_extension(f'cogs.{extension}')
                print(f'loaded {extension}')
            except Exception as e:
                error = f'{extension}\n {type(e).__name__} : {e}'
                print(f'failed to load extension {error}')
            print('-' * 10)

    async def on_ready(self):
        """
        This event is called every time the bot connects or resumes connection.
        """
        print('-' * 10)
        self.app_info = await self.application_info()
        print(f'Logged in as: {self.user.name}\n'
              f'Using discord.py version: {discord.__version__}\n'
              f'Owner: {self.app_info.owner}\n'
              f'Template Maker: SourSpoon / Spoon#0001')
        print('-' * 10)

    async def on_message(self, message):
        """
        This event triggers on every message received by the bot. Including one's that it sent itself.
        If you wish to have multiple event listeners they can be added in other cogs. All on_message listeners should
        always ignore bots.
        """
        if message.author.bot:
            return  # ignore all bots
        await self.process_commands(message)
    
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            hours, minutes, seconds = str(datetime.timedelta(seconds=round(error.retry_after))).split(":")
            timeLeft = f"{hours} hours, {minutes} minutes, and {seconds} seconds"
            await ctx.send(f"The people of QZ can construct another item in {timeLeft}.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"You didn't specify the `{error.param.name}` argument.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("You didn't give a valid argument.")
        elif isinstance(error, commands.NotOwner):
            await ctx.send("Yeah I don't think you're allowed to do that buddy.")
        elif isinstance(error, commands.MissingPermissions):
            missing_perms = ', '.join(error.missing_perms)
            await ctx.send(f"You're missing the following permissions: {missing_perms}")
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send("Uh kid that role doesn't exist in this server")
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send("Whoa what's up with the wall of text? Stop giving me so many arguments!")
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

if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

