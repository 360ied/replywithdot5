from utility import blib, music


async def handler_dl(query, voice_client, text_channel, member):
    prepared_coroutine = blib.PreparedCoroutine(blib.audio_getter_creator, query)
    return music.Piece(
        query, prepared_coroutine.run, voice_client, text_channel, member
    )
