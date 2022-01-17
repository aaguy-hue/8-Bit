import bot
import asyncio
from website import app

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.run())

if __name__ == "__main__":
    app.run()
