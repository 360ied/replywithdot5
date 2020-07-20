"""OWNER COMMAND: Shuts down the bot"""

from os import getenv

import discord

description = __doc__

usage = "{prefix}kill\n"

aliases = dict()

required_parameters = set()

required_permissions = set()

expected_positional_parameters = list()

authorized_ids = {int(x) for x in getenv("owner_access").split(",")}


async def run(client: discord.Client, group, message: discord.Message, args: dict):
    if message.author.id not in authorized_ids:
        await message.channel.send("This command is meant for others.")
    else:
        await message.channel.send("Shutting down...")
        exit(0)
