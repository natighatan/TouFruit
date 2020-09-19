import discord


def get_members_for_guild(bot, guild_id: str) -> list:
    """
    Returns a members dictionary for a given guild
    :param bot: Discord bot object
    :param guild_id: String of guild name
    :return: List of Discord guild member objects
    """
    guild = discord.utils.get(bot.guilds, id=guild_id)
    return guild.members
