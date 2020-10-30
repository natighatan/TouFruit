"""
This file defines the main functionalities of the bot, such as
initialization, connection and authentication, and loading
Cogs-based extensions.

Changes on this file should be conservative.

Bot invite link: https://discord.com/oauth2/authorize?client_id=756225088239566879&scope=bot
"""
import os
import json

import discord
from discord.ext import commands
from dotenv import load_dotenv
import helper_methods

# Load environment variables
load_dotenv()

# Constants
DESCRIPTION = '''This message will be presented when evoking the help command.
This will be on the second line.'''
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD'))
helper_methods.PERMITTED_GUILDS = json.loads(os.getenv('PERMITTED_GUILDS'))

# this specifies what extensions to load when the bot starts up
"""
Note that any Cog-based extension to be loaded must be
explicitly mentioned within this variable.
Include only submodule names, without file extensions
(e.g. "fun" and not "fun.py")
"""
STARTUP_EXTENSIONS = ['fun']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', description=DESCRIPTION, intents=intents)


@bot.event
async def on_ready():
    """
    Defines action of the bot when it starts up
    :return:
    """
    guild_members = helper_methods.get_members_for_guild(bot=bot, guild_id=GUILD_ID)
    members = '\n - '.join([member.name for member in guild_members])
    print(f'{bot.user.name} has connected to Discord!')
    print(f'It has identified the following members under the server {GUILD_ID}:\n - {members}')


@bot.command()
async def load(ctx, extension_name: str):
    """
    Loads an extension
    :param ctx: Context variable
    :param extension_name: String defining name of extension to be loaded
    :return:
    """
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as exception:
        await ctx.send("```py\n{}: {}\n```".format(type(exception).__name__, str(exception)))
        return
    await ctx.send("{} loaded.".format(extension_name))


@bot.command()
async def unload(ctx, extension_name: str):
    """
    Unloads an extension
    :param ctx: Context variable
    :param extension_name: String defining name of extension to be unloaded
    :return:
    """
    bot.unload_extension(extension_name)
    await ctx.send("{} unloaded.".format(extension_name))


if __name__ == "__main__":
    for extension in STARTUP_EXTENSIONS:
        try:
            bot.load_extension(extension)
        except ModuleNotFoundError as exception:
            EXCEPTION_MESSAGE = '{}: {}'.format(type(exception).__name__, exception)
            print('Failed to load extension {}\n{}'.format(extension, EXCEPTION_MESSAGE))

    bot.run(TOKEN)
