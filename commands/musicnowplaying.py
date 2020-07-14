"""Shows the current playing piece"""
import discord

from utility import music
from utility.music import MusicQueue

description = __doc__

usage = "{prefix}np\n"

aliases = dict()

required_parameters = set()

required_permissions = set()

expected_positional_parameters = list()


async def run(client: discord.Client, group, message: discord.Message, args: dict):
    # noinspection PyUnresolvedReferences
    music_manager: music.MusicManager = client.music_manager

    try:
        queue: MusicQueue = music_manager.queues[message.guild.id]
    except KeyError:
        await message.channel.send("There is nothing playing!")
        return "There is nothing playing!"

    await message.channel.send(
        content=f"Currently Playing:",
        embed=queue.current_piece.embed
    )
