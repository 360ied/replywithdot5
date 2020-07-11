"""Responds with Pong!"""
import discord

from utility.persistentstoragev2 import PersistentStorage

description = __doc__

usage = "{prefix}ping"

aliases = {
    "prefix": "prefix",
}

required_parameters = {
    "prefix"
}

required_permissions = {
    "manage_guild"
}

expected_positional_parameters = [
    "prefix"
]


async def run(client: discord.Client, group, message: discord.Message, args: dict) -> None:
    prefix: str = args["prefix"]
    persistent_storage: PersistentStorage = client.persistent_storage

    await persistent_storage.update_config(message.guild.id, {"prefix": prefix})

    await message.channel.send(f"Updated prefix to `{prefix}`")
