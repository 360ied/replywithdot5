"""Searches up Meanings on Wiktionary"""
from urllib import parse

import discord

from utility import wordnetasync

description = __doc__

usage = "{prefix}meaning (query)"

aliases = {
    "query": "query",
    "q": "query"
}

required_parameters = {
    "query"
}

required_permissions = set()

expected_positional_parameters = [
    "query"
]


async def run(client: discord.Client, group, message: discord.Message, args: dict) -> None:
    query: str = parse.quote(args["query"])
    definitionary = await wordnetasync.meaning(query)
    # Imported from replywithdot2 (replywithdotrecoded)
    definition = f"**{query}**:"
    if definitionary is None:
        definition += "\nNo Definition Found."
    else:
        for key, value in definitionary.items():
            to_add = f"\n*{key}*:\n"
            definitions = ", ".join(value)
            to_add += discord.utils.escape_markdown(definitions)
            if len(definition) + len(to_add) > 2000:
                await message.channel.send(definition)
                definition = ""
            definition += to_add
    await message.channel.send(definition)
