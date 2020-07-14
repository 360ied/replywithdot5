import hashlib

import youtube_dl

from utility import blib, music


async def handler_dl(query, voice_client, text_channel, member, loop):
    prepared_coroutine = blib.PreparedCoroutine(blib.audio_getter_creator, query)
    return music.Piece(
        query, prepared_coroutine, voice_client, text_channel, member
    )


async def handler_yt(query, voice_client, text_channel, member, loop):
    await loop.run_in_executor(None, helper_ytdl, query)
    # This will not download anything, as it will have already be downloaded
    prepared_coroutine = blib.PreparedCoroutine(blib.audio_getter_creator, query)
    return music.Piece(
        query, prepared_coroutine, voice_client, text_channel, member
    )


def helper_ytdl(query):
    ytdl_format_options = {
        'format': 'bestaudio/best',
        'outtmpl': f"cache/{hashlib.sha3_256(bytes(query, 'utf-8')).hexdigest()}",
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
        'usenetrc': True
    }
    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
    ytdl.download([query])
