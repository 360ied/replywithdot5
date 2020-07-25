"""Takes a snapshot of a guild"""
import discord
import yaml

from utility.blib import deep_dict_from_object, upload_discord

description = __doc__

usage = "{prefix}snapshot [id]"

aliases = {
    "id": "id"
}

required_parameters = set()

required_permissions = set()

expected_positional_parameters = ["id"]


async def run(client: discord.Client, group, message: discord.Message, args: dict) -> None:
    target_guild = client.get_guild(int(args["id"]))
    if target_guild is None:
        await message.channel.send("Guild not found!")
        return

    await upload_discord(
        message.channel,
        yaml.dump(
            deep_dict_from_object(
                target_guild
            )
        ),
        args["id"]
    )
