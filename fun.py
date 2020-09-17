"""
This file defines commands for fun that the bot can carry out
Expand this freely but always test to verify your function
isn't exposed to harm by malicious input!
"""
from discord.ext import commands


class Fun(commands.Cog):
    """
    This Cog-based class contains all the fun-related functions.
    All new functionalities should be defined under here.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add", help="Returns the sum for two numbers")
    async def add(self, ctx, left: int, right: int) -> int:
        """
        Adds two numbers together and returns their sum
        :param ctx: Context variable
        :param left: Left integer to add
        :param right: Right integer to add
        :return: integer result of sum between left and right
        """
        await ctx.send(left + right)


def setup(bot):
    """
    Function that defines a setup case for this Cog-related class
    This is a mandatory definition for this submodule to work,
    do NOT remove this.
    :param bot: The external bot requesting the extension
    :return:
    """
    bot.add_cog(Fun(bot))
