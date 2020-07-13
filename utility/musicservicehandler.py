import aiohttp
import discord

from utility import blib, music


async def handler_dl(query, voice_client, text_channel, member):
    return music.Piece(
        query, blib.audio_getter_creator(query), voice_client, text_channel, member
    )
