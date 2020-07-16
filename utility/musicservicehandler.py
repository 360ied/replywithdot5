import hashlib
import json
import logging
import pathlib
import re
import traceback
from os import getenv

import aiohttp
import youtube_dl

from utility import blib, music, ytdlhelper, spotify

cache_folder = "cache/"


async def handler_dl(query, voice_client, text_channel, member, loop):
    file_url_hash = hashlib.sha3_256(bytes(query, "utf-8")).hexdigest()
    file_name = f"{cache_folder}{file_url_hash}"
    if pathlib.Path(file_name).is_file():
        logging.info(f"{file_name} already exists. Using cached version.")
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(query) as response:
                with open(file_name, "wb") as file:
                    while 1:
                        chunk = await response.content.read(blib.one_megabyte_chunk_size)
                        if not chunk:
                            break
                        file.write(chunk)

    prepared_coroutine = blib.PreparedCoroutine(blib.audio_getter_creator, query)
    return [music.Piece(
        query, None, prepared_coroutine, voice_client, text_channel, member
    )]


async def handler_yt(query, voice_client, text_channel, member, loop, pack=True):
    video_info = await loop.run_in_executor(None, helper_ytdl, query)
    # debug
    # logging.debug(video_info)
    # logging.debug(type(video_info))
    # with open("latest_json.json", "w") as fp:
    #     json.dump(video_info, fp)

    if video_info is None:
        # Could not find query
        logging.error(f"Could not find {query}")
        await text_channel.send(f"Could not find {query}\n"
                                f"Skipping!")
        return None

    # Handle playlists
    if video_info["extractor"] == "youtube:playlist":
        to_return = list()
        async for i in helper_handler_yt_playlist(video_info, voice_client, text_channel, member, loop):
            to_return.append(i)
        return to_return

    # link = f"https://youtube.com/watch?v={video_info['entries'][0]['id']}"

    # This will not download anything, as it will have already be downloaded
    prepared_coroutine = blib.PreparedCoroutine(blib.audio_getter_creator, query)

    try:
        embed = ytdlhelper.parse(video_info, query, voice_client, text_channel, member, loop)
    except Exception:
        traceback.print_exc()
        with open("latest_json.json", "w") as fp:
            json.dump(video_info, fp)
        logging.error("Error! Trying again")
        return await handler_yt(query, voice_client, text_channel, member, loop, pack=pack)

    piece = music.Piece(query, embed, prepared_coroutine, voice_client, text_channel, member)

    if pack:
        return [piece]
    else:
        return piece


async def helper_handler_yt_playlist(info, voice_client, text_channel, member, loop):
    assert info["extractor"] == "youtube:playlist"
    videos = info["entries"]
    logging.info(f"Processing playlist of {len(videos)} videos")
    for i in videos:
        yield await handler_yt(i["webpage_url"], voice_client, text_channel, member, loop, pack=False)


def helper_ytdl(query, **options):
    ytdl_format_options = {
        'format': 'bestaudio/best',
        'outtmpl': f"{cache_folder}{hashlib.sha3_256(bytes(query, 'utf-8')).hexdigest()}",
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'logtostderr': False,
        'quiet': False,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
        'usenetrc': True
    }
    ytdl_format_options.update(options)
    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
    # ytdl.download([query])
    output = ytdl.extract_info(query, download=True)
    return output


spotify = spotify.Spotify(getenv("spotify_client_id"), getenv("spotify_client_secret"))


# Modified from https://github.com/Just-Some-Bots/MusicBot/blob/master/musicbot/bot.py
async def handler_spotify(query, voice_client, text_channel, member, loop):
    if 'open.spotify.com' in query:
        modq = 'spotify:' + re.sub('(http[s]?:\/\/)?(open.spotify.com)\/', '', query).replace('/', ':')
        # remove session id (and other query stuff)
        modq = re.sub('\?.*', '', modq)
    else:
        modq = query

    songs = list()

    if modq.startswith('spotify:'):
        parts = modq.split(":")
        if 'track' in parts:
            res = await spotify.get_track(parts[-1])
            songs.append(f"{res['artists'][0]['name']} {res['name']}")
        elif 'album' in parts:
            res = await spotify.get_album(parts[-1])
            for i in res['tracks']['items']:
                songs.append(f"{i['artists'][0]['name']} {i['name']}")
        elif 'playlist' in parts:
            res = []
            r = await spotify.get_playlist_tracks(parts[-1])
            while True:
                res.extend(r['items'])
                if r['next'] is not None:
                    r = await spotify.make_spotify_req(r['next'])
                    continue
                else:
                    break

            for i in res:
                songs.append(f"{i['track']['artists'][0]['name']} {i['track']['name']}")

    logging.info(str(songs))

    return [await handler_yt(i, voice_client, text_channel, member, loop, pack=False) for i in songs]
