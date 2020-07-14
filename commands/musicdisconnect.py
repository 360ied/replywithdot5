"""Remove the bot from the voice channel"""
import discord

description = __doc__

usage = "{prefix}dc\n"

aliases = dict()

required_parameters = set()

required_permissions = {
    "move_members"
}

expected_positional_parameters = list()


async def run(client: discord.Client, group, message: discord.Message, args: dict):
    await message.guild.me.edit(voice_channel=None)
    await message.channel.send("Disconnected")
