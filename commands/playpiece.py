"""Play Audio"""
import discord

from utility import blib, music, musicservicehandler

description = __doc__

usage = "{prefix}play (service) (query)\n" \
        "Supported Services: dl\n" \
        "dl: Direct Download"

aliases = {
    "service": "service",
    "query": "query"
}

required_parameters = {
    "service", "query"
}

required_permissions = set()

expected_positional_parameters = [
    "service", "query"
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

    try:
        handler = getattr(musicservicehandler, f"handler_{args['service']}")
    except AttributeError:
        await message.channel.send("Invalid service!")
        return "Invalid Service"

    piece = await handler(query, music_queue.voice_client, message.channel, message.author)

    music_queue.add_piece(piece)

    client.loop.create_task(music_queue.player())
