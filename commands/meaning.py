"""Searches up Meanings on Wiktionary"""
from io import BytesIO
from os import getenv
from urllib import parse

import aiohttp
import discord

from utility.wiktionaryparserasync import WiktionaryParser

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
    parser = WiktionaryParser()
    response = await parser.fetch(query)
    print(response)
