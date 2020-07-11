"""Wolfram Alpha"""
from io import BytesIO
from os import getenv
from urllib import parse

import aiohttp
import discord

description = __doc__

usage = "{prefix}wolfram (query)"

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
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://api.wolframalpha.com/v1/simple?i={query}&width=800&appid={getenv('WOLFRAM_ALPHA_APP_ID')}"
        ) as response:
            if await response.text(errors="ignore") == "Wolfram|Alpha did not understand your input":
                await message.channel.send("Wolfram|Alpha did not understand your input")
            else:
                file = BytesIO(await response.read())
                await message.channel.send(file=discord.File(file, filename="result.png"))
