# Contributing to 8-Bit

Thank you for spending your time to help make 8-Bit even better! 😀

The following is mostly just a guideline to help you contribute to the bot, while also keeping to some important rules. Do not skip over this, as it may result in you having issues when trying to contribute.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Running the Bot](#running-the-bot)
  - [Getting Dependencies](#getting-dependencies)
  - [Setting Environment Variables](#setting-environment-variables)
  - [Finally Running It!](#finally-running-it)
- [Finding what to Develop](#finding-what-to-develop)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)

## Code of Conduct

Quite frankly, please just treat everyone with respect and kindness. Do not get mad at people for making mistakes, and respect everyone's opinions.

## Running the Bot

### Getting Dependencies

You can get the dependencies automatically by going to the path of the project in your terminal, then running `python -m pip install -r requirements.txt`.

If you have any suggestions on adding/removing a dependency, then please make an issue. Ideally, the bot should be as lightweight as possible, and if you want to suggest swapping out or removing a dependency for that, then I'm up for it. If you want to add one, please explain why the bot would benefit from the added dependency.

The bot depends on the following things:
 - [Python 3.6 or newer](https://www.python.org/downloads/) (programming language)
 - [discord.py](https://github.com/Rapptz/discord.py) (interface to Discord API)
 - [discord-components](https://gitlab.com/discord.py-components/discord.py-components) (library which allows for use of buttons and dropdowns, which will be in discord.py in a few months)
 - [Pillow](https://github.com/python-pillow/Pillow) (used to generate images)
 - [Flask](https://flask.palletsprojects.com/en/2.0.x/) (used as a web server for the images)

### Setting Environment Variables

After you've got all your dependencies, you just have one more step before you can finally get started. You will need to set the following environment variables:
 
 - 8BIT_TOKEN (the token of your discord bot you will test this on, go to [discord.com/developers](https://discord.com/developers) to do this)
 - IMAGE_API_PASSWORD (this is a password that will be used for the image api, it makes sure that people don't start using your api)
 - FLASK_SECRET (generate this by typing `python -c 'import os; print(os.urandom(16))'` in your terminal, it's for the purpose of keeping the website with the image api secure)

On Windows, you can do `SET VARIABLE=VALUE` in your terminal to set temporary environment variables. Unfortunately, you will have to do more steps to make it persistent. Go into Settings -> System -> About, then click "Advanced system settings" under the "Related settings" section. This will take you to the "Advanced" tab of System Properties. In the window that popped up, press the "Environment Variables" button towards the bottom. You will likely want to set the environment variable as a user variable, but putting it as a system variable works too. Press the "new" button, and the rest is easy to do.

On *nix systems like MacOS and Linux, you can do `export VARIABLE=VALUE` to set environment variables.


### Finally Running It!

Finally, go to the src folder and run the file called "QtKm_Awakened.py". Running this file will run the project. If you have any questions, just message in our [discord server](https://discord.com/invite/VPPrpmQ44q).

## Finding what to Develop

If you're new and you want to find what to develop, then there are two great places to find this. First of all, head over to [the issues page](https://github.com/aaguy-hue/8-Bit/issues) to find issues with the bot that can be fixed. Also, you can head over to [the projects page](https://github.com/aaguy-hue/8-Bit/projects) to find what's currently on the roadmap.

## Submitting Changes

If you want to make a change to the bot, follow the following instructions.

First, go on github and make a fork of the project, or a new branch. Then, make your changes within that. Afterwards, make a pull request describing what your change does. Your pull request should follow the criteria below.

Pull Request Criteria:
 - What does it do?
 - Why is this useful?
 - What tests have you performed to make sure that what you modified/added is still functional?
   - If you add/modify something which uses the image API, then just test if the images still work locally as you cannot test the image API yourself

Your pull request may not be accepted if you do not meet the criteria.

## Reporting Bugs

To report bugs, simply head over to [the issues page of this repository.](https://github.com/aaguy-hue/8-Bit/issues) When reporting bugs, please make sure to give a detailed description of the bug while also staying concise. In addition, you should make sure that it's not a duplicate bug.
