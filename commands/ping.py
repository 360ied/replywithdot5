"""Responds with Pong!"""
import discord


description = __doc__

aliases = dict()

accepted_parameters = list()

required_parameters = list()

required_permissions = set()

expected_positional_parameters = list()


async def run(client: discord.Client, group, message: discord.Message, args: dict) -> None:
    await message.channel.send("Pong!")
