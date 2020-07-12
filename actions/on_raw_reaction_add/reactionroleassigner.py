"""
Assigns Reaction Roles
"""
import discord

from utility.persistentstoragev2 import PersistentStorage


async def run(client: discord.Client, raw_reaction_action_event: discord.RawReactionActionEvent):
    if raw_reaction_action_event.guild_id is None:
        return "Reaction not reacted within a guild"
    persistent_storage: PersistentStorage = client.persistent_storage

    config = await persistent_storage.get_config(raw_reaction_action_event.guild_id)

    if "reaction_roles" not in config:
        return "No reaction roles present in guild"

    reaction_roles_config = config["reaction_roles"]

    for message_id, role_id, emoji_string in reaction_roles_config:
        if raw_reaction_action_event.message_id == message_id:
            if str(raw_reaction_action_event.emoji) == emoji_string:
                guild: discord.Guild = client.get_guild(raw_reaction_action_event.guild_id)
                role: discord.Role = guild.get_role(role_id)
                await raw_reaction_action_event.member.add_roles(role)
