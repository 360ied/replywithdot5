"""Play Audio"""
import logging

import discord

from utility import music, musicservicehandler

description = __doc__

usage = "{prefix}play (query) [--dl]\n" \
        "Full list of sites supported: https://ytdl-org.github.io/youtube-dl/supportedsites.html\n" \
        "If you want to use a direct download, append --dl to the end of the command\n" \
        "If you want to play a playlist"

aliases = {
    "query": "query",
    "dl": "dl"
}

required_parameters = {
    "query"
}

required_permissions = set()

expected_positional_parameters = [
    "query"
]


async def run(client: discord.Client, group, message: discord.Message, args: dict):
    # noinspection PyUnresolvedReferences
    music_manager: music.MusicManager = client.music_manager
    # Check if requester is in a voice channel
    if message.author.voice is None:
        await message.channel.send("You are not in a voice channel!")
        return "Requester is not in a voice channel"
    else:
        music_queue = await music_manager.connect_with_member(message.author, message.channel)

    await message.channel.send("Searching query...")

    query = args["query"]

    service = "dl" if "dl" in args else "yt"

    try:
        handler = getattr(musicservicehandler, f"handler_{service}")
    except AttributeError:
        logging.error(f"UNEXPECTED SERVICE: {service}")
        await message.channel.send("If you are seeing this message, something has gone horribly wrong.")
        return "Invalid Service"

    pieces = await handler(query, music_queue.voice_client, message.channel, message.author, client.loop)

    music_queue.add_pieces(pieces)

    await message.channel.send(f"Added {len(pieces)} pieces to queue!")

    client.loop.create_task(music_queue.player())

    return "Success"
