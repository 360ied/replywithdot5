"""Wolfram Alpha"""
from io import BytesIO
from os import getenv
from urllib import parse

import aiohttp
import discord

description = __doc__

usage = "{prefix}wolfram (query) [--t]\n" \
        "Add --t if you want the response to be in text format"

aliases = {
    "query": "query",
    "q": "query",
    "t": "txt",
    "text": "txt",
    "txt": "txt"
}

required_parameters = {
    "query"
}

required_permissions = set()

expected_positional_parameters = [
    "query"
]

wolfram_alpha_app_id = getenv('WOLFRAM_ALPHA_APP_ID')


async def run(client: discord.Client, group, message: discord.Message, args: dict) -> None:
    query: str = parse.quote(args["query"])
    async with aiohttp.ClientSession() as session:
        # Wolfram Text API
        if "txt" in args:
            link = f"https://api.wolframalpha.com/v1/result?appid={wolfram_alpha_app_id}&i={query}"
        # Wolfram Image API
        else:
            link = f"https://api.wolframalpha.com/v1/simple?i={query}&width=800&appid={wolfram_alpha_app_id}"
        async with session.get(link) as response:
            try:
                response_text = await response.text()
                await message.channel.send(response_text)
            except UnicodeDecodeError:
                file = BytesIO(await response.read())
                await message.channel.send(file=discord.File(file, filename="result.png"))
