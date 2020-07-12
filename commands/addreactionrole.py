"""Adds a reaction role to a message"""
from urllib import parse

import discord

from utility import wordnetasync
from utility.persistentstoragev2 import PersistentStorage

description = __doc__

usage = "{prefix}addreactionrole (message id) (role id) (emoji)"

aliases = {
    "message_id": "message_id",
    "role_id": "role_id",
    "emoji": "emoji"
}

required_parameters = {
    "message_id", "role_id", "emoji"
}

required_permissions = {
    "manage_roles"
}

expected_positional_parameters = [
    "message_id", "role_id", "emoji"
]


async def run(client: discord.Client, group, message: discord.Message, args: dict) -> None:
    target_role: discord.Role = message.guild.get_role(int(args["role_id"]))
    if target_role is None:
        await message.channel.send(f"Role not found!")
    elif target_role.position >= message.author.top_role.position:
        await message.channel.send(f"You do not have permissions to assign this role!")
    else:
        persistent_storage: PersistentStorage = client.persistent_storage
        target_message_id = int(args["message_id"])
        target_emoji_string = args["emoji"]

        config = await persistent_storage.get_config(message.guild.id)
        if "reaction_roles" not in config:
            config["reaction_roles"] = list()
        config["reaction_roles"].append([target_message_id, target_role.id, target_emoji_string])
        
        await message.channel.send("Done!")
