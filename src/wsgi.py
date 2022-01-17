from website import app
import threading
import bot

bot_thread = threading.Thread(target=bot.run, name="Discord Bot")
bot_thread.start()

if __name__ == "__main__":
    app.run()
