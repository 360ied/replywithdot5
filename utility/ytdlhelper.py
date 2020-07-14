import discord

from utility import blib


def parse(response: dict, query, voice_client, text_channel, member, loop):
    """
    Automatically finds a parser and returns the output
    """
    parse_type = blib.multireplace(response["extractor"], {
        ":": "_"
    })
    try:
        parser = globals()[f"parser_{parse_type}"]
    except KeyError:
        parser = _parser_generic

    return parser(response, query, voice_client, text_channel, member, loop)


def _parser_generic(response: dict, query, voice_client, text_channel, member, loop):
    embed = discord.Embed()
    embed.title = response["id"]
    embed.set_author(name=str(member), icon_url=str(member.avatar_url))
    embed.set_footer(
        text=f"{response['extractor_key']}\n"
             f"From query: {query}"
    )

    return embed


def parser_youtube(response: dict, query, voice_client, text_channel, member, loop):
    embed = discord.Embed()
    embed.title = response["title"]
    embed.url = response["webpage_url"]
    embed.set_thumbnail(url=response["thumbnail"])

    embed.set_author(name=str(member), icon_url=str(member.avatar_url))

    embed.add_field(name="Length", value=blib.format_time(seconds=response["duration"]))

    embed.set_footer(
        text=f"{response['extractor_key']}\n"
             f"From query: {query}"
    )

    return embed


def parser_youtube_search(response: dict, query, voice_client, text_channel, member, loop):
    embed = discord.Embed()
    video = response["entries"][0]
    embed.title = video["title"]
    embed.url = video["webpage_url"]
    embed.set_thumbnail(url=video["thumbnail"])

    embed.set_author(name=str(member), icon_url=str(member.avatar_url))

    embed.add_field(name="Length", value=blib.format_time(seconds=video["duration"]))

    embed.set_footer(
        text=f"{video['extractor_key']}\n"
             f"From query: {query}"
    )

    return embed
