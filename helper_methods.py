"""
Helper methods file for the TouFruit bot
"""
import discord
from difflib import SequenceMatcher
from geopy.geocoders import Nominatim

"""
Computations
"""


def compute_geo_center_of_mass(list_of_cities):
    # Initialize variables
    geolocator = Nominatim(user_agent="TouFruit")
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0
    sum5 = 0

    # Compute center of mass
    for i in range(len(list_of_cities)):
        location = geolocator.geocode(list_of_cities[i], language="en")
        if i == (len(list_of_cities) - 1):
            next_location = geolocator.geocode(list_of_cities[0], language="en")
        else:
            next_location = geolocator.geocode(list_of_cities[i + 1], language="en")
        sum1 += (float(location.longitude) * float(next_location.latitude) - float(next_location.longitude) * float(
            location.latitude))
        sum2 += (float(location.longitude) * float(next_location.latitude) - float(next_location.longitude) * float(
            location.latitude)) * (float(location.longitude) + float(next_location.longitude))
        sum3 += (float(location.longitude) * float(next_location.latitude) - float(next_location.longitude) * float(
            location.latitude)) * (float(location.latitude) + float(next_location.latitude))
        # Average
        sum4 += float(location.longitude)
        sum5 += float(location.latitude)

    Area = sum1 / 2
    C_North = sum3 / (6 * Area)
    C_East = sum2 / (6 * Area)

    # Average
    C_test_North = sum5 / len(list_of_cities)
    C_test_East = sum4 / len(list_of_cities)

    # com_string = f"Center of mass: {C_North} North, {C_East} East"
    # average_coordinates_string = f"Average coordinates: {C_test_North} North, {C_test_East} East"
    # return com_string, average_coordinates_string
    return f"https://www.google.com/maps/search/google+maps+{C_North},{C_East}"


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

    if requested_name.startswith('<@!') and requested_name.endswith('>'):
        # This is a mention
        user_id = int(requested_name[3:-1])
        best_match = [member for member in members if member.id == user_id][0]
        return best_match

    best_match = None
    best_similarity = -1.00
    for member in members:
        similarity = max(compute_string_similarity_ratio(string_a=requested_name, string_b=member.name),
                         compute_string_similarity_ratio(string_a=requested_name, string_b=member.nick))
        if (similarity < threshold) or (similarity <= best_similarity):
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
