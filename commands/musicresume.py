"""Resumes the player"""
import discord

from utility import music
from utility.music import MusicQueue

description = __doc__

usage = "{prefix}pause\n"

aliases = dict()

required_parameters = set()

required_permissions = set()

expected_positional_parameters = list()


async def run(client: discord.Client, group, message: discord.Message, args: dict):
    # noinspection PyUnresolvedReferences
    music_manager: music.MusicManager = client.music_manager
    # Check if requester is in a voice channel
    if message.author.voice is None:
        await message.channel.send("You are not in a voice channel!")
        return "Requester is not in a voice channel"

    try:
        queue = music_manager.queues[message.guild.id]
    except KeyError:
        await message.channel.send("There is nothing playing!")
        return "There is nothing playing!"

    queue: MusicQueue
    queue.current_piece.resume()
    await message.channel.send("Resumed the player")
