"""
This file defines commands for fun that the bot can carry out
Expand this freely but always test to verify your function
isn't exposed to harm by malicious input!
"""
from discord.ext import commands
import random
import helper_methods


class Fun(commands.Cog):
    """
    This Cog-based class contains all the fun-related functions.
    All new functionalities should be defined under here.
    """

    def __init__(self, bot):
        self.bot = bot
        self.interactions = ["pout", "highfive", "hug", "kiss", "pat", "shoot", "bite", "slap", "lick", "feed", "stare",
                             "sip", "spank", "drink", "stab", "poke", "punch", "shrug", "facepalm", "cry", "wave",
                             "sleep", "laugh", "blush", "dance", "explode", "sniff", "tackle", "hide"]
        self.vowels = ("a", "e", "i", "o", "u")

    @commands.command(name="geocom", help="Computes Geo center of mass for a list of cities")
    async def geocom(self, ctx, *args):
        if not args:
            await ctx.send('Please provide names of cities using quotes. For example: $geocom "Tel Aviv" "New York"')
            return

        locations = list(args)
        link = helper_methods.compute_geo_center_of_mass(list_of_cities=locations)
        await ctx.send(f"See your CoM here: {link}")

    @commands.command(name="whattodo", help="Randomly decides what to do to someone")
    async def whattodo(self, ctx, user):
        # Find the mentioned member
        member = helper_methods.find_member_by_name_similarity(bot=self.bot,
                                                               requested_name=user,
                                                               guild_id=ctx.guild.id)
        if not member:
            await ctx.send(f"I could not find anyone with a name even remotely similar to {user}. Sorry!")
            return

        member_name = helper_methods.get_member_name(member=member)
        action = random.choice(self.interactions)
        action = f"{'an' if action.startswith(self.vowels) else 'a'} {action}"
        await ctx.send(f"Oh! I think {member_name} deserves {action}")

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
