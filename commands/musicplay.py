"""Play Audio"""
import logging

import discord

from utility import music, musicservicehandler

description = __doc__

usage = "{prefix}play (query) [--dl] [--spotify]\n" \
        "Full list of sites supported: https://ytdl-org.github.io/youtube-dl/supportedsites.html\n" \
        "If you want to use a direct download, append --dl to the end of the command\n" \
        "If you want to use spotify, append --spotify (or --sp) to the end of the command" \
        "Please do not play 10 hour videos or overly long playlists, they will take forever to load."

aliases = {
    "query": "query",
    "dl": "dl",
    "spotify": "spotify",
    "sp": "spotify"
}

required_parameters = {
    "query"
}

required_permissions = set()

expected_positional_parameters = [
    "query"
]

service_flags = {"dl", "spotify"}


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

    service = "yt"
    for i in service_flags:
        if i in args:
            service = i
            break

    try:
        handler = getattr(musicservicehandler, f"handler_{service}")
    except AttributeError:
        logging.error(f"UNEXPECTED SERVICE: {service}")
        await message.channel.send("If you are seeing this message, something has gone horribly wrong.")
        return "Invalid Service"

    pieces = await handler(query, music_queue.voice_client, message.channel, message.author, client.loop)

    filtered_pieces = list()
    for i in pieces:
        if isinstance(i, music.Piece):
            filtered_pieces.append(i)

    music_queue.add_pieces(filtered_pieces)

    await message.channel.send(f"Added {len(filtered_pieces)} pieces to queue!")

    client.loop.create_task(music_queue.player())

    return "Success"
