"""Takes a snapshot of a guild"""
from io import StringIO

import discord
import jsonpickle
import yaml

from commands.ownerkill import authorized_ids
from utility.blib import upload_discord

description = __doc__

usage = "{prefix}snapshot [id]"

aliases = {
    "id": "id"
}

required_parameters = set()

required_permissions = set()

expected_positional_parameters = ["id"]


# Remove unsafe output from jsonpickle
def filter_output(dictionary):
    for k, v in dictionary.items():
        if isinstance(v, dict):
            if "py/object" in v:
                if v["py/object"] == "discord.state.ConnectionState":
                    del dictionary[k]
            else:
                dictionary[k] = filter_output(v)

    return dictionary


async def run(client: discord.Client, group, message: discord.Message, args: dict) -> None:
    if message.author.id not in authorized_ids:
        await message.channel.send("This command is meant for others.")
    else:
        target_guild = client.get_guild(int(args["id"]))
        if target_guild is None:
            await message.channel.send("Guild not found!")
            return

        # await message.channel.send("command temporarily disabled")
        # return

        await upload_discord(
            message.channel,
            StringIO(
                yaml.dump(
                    filter_output(
                        jsonpickle.pickler.Pickler().flatten(
                            target_guild
                        )
                    )
                ),
            ),
            f"{args['id']}.yaml"
        )
