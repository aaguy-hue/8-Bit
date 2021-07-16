# 8-Bit

A discord bot to have fun with friends! The bot is hosted on heroku, use this link to invite the bot: https://discord.com/api/oauth2/authorize?client_id=705890912282345472&permissions=515136&scope=bot.

## Functionality

 - Connect 4 game (AI coming in future!)
 - Tic Tac Toe (with an AI, difficulty modes coming soon!)
 - Rock Paper Scissors
 - ~~Voting to create channel!~~ (feature removed due to potentially creating ping spam in its form as it was previously)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## Running the Bot

### Getting Dependencies

You can get the dependencies automatically by going to the path of the project in your terminal, then running `python -m pip install -r requirements.txt`. If you add a new package, please add it and its dependencies to [the requirements.txt file](requirements.txt).

The bot depends on the following things:
 - Python Interpreter (programming language)
 - [discord.py](https://github.com/Rapptz/discord.py) (interface to Discord API)
 - [discord-components](https://gitlab.com/discord.py-components/discord.py-components) (library which allows for use of buttons and dropdowns, which will be in discord.py in a few months)
 - [Pillow](https://github.com/python-pillow/Pillow) (used to generate images)
 - [Requests](https://github.com/psf/requests) (used to upload images to the imgur api for tic tac toe)

### Setting Environment Variables

After you've 
