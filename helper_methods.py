"""
Helper methods file for the TouFruit bot
"""
import discord
from difflib import SequenceMatcher

"""
Computations
"""


def compute_string_similarity_ratio(string_a, string_b):
    """
    Returns the edit-distance-based similarity between two strings
    :param string_a: First string
    :param string_b: Second string
    :return: Float value for similarity between the strings
    """
    if (not string_a) or (not string_b):
        return 0.00
    return SequenceMatcher(None, string_a, string_b).ratio()


def find_member_by_name_similarity(bot, requested_name, guild_id, threshold=0.5):
    """
    For a given guild, finds the member with the highest similarity score
    to the requested name
    :param bot: Discord bot object
    :param requested_name: String of requested name
    :param guild_id: Integer ID of guild
    :return: Discord Member object
    """
    members = get_members_for_guild(bot=bot, guild_id=guild_id)
    best_match = None
    best_similarity = -1.00
    for member in members:
        similarity = max(compute_string_similarity_ratio(string_a=requested_name, string_b=member.name),
                         compute_string_similarity_ratio(string_a=requested_name, string_b=member.nick))
        if (similarity<threshold) or (similarity <= best_similarity):
            continue
        best_match = member
        best_similarity = similarity

    return best_match


"""
Acquisition
"""


def get_member_name(member) -> str:
    """
    For a given member, get the best fit name, i.e.
    nickname if they have one, or otherwise their name
    :param member: Discord member object
    :return: String of the best-fit name
    """
    if not member:
        return None
    return member.nick if member.nick else member.name


def get_members_for_guild(bot, guild_id: str) -> list:
    """
    Returns a members dictionary for a given guild
    :param bot: Discord bot object
    :param guild_id: String of guild name
    :return: List of Discord guild member objects
    """
    guild = discord.utils.get(bot.guilds, id=guild_id)
    return sorted([member for member in guild.members if not member.bot],
                  key=lambda x: x.name, reverse=False)
