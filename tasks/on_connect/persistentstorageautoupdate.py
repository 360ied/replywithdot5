import asyncio
import traceback

import discord

from utility.persistentstoragev2 import PersistentStorage


async def run(client: discord.Client):
    persistent_storage: PersistentStorage = client.persistent_storage

    while not await asyncio.sleep(10):
        try:
            await persistent_storage.write_config_cache()
        except Exception:
            traceback.print_exc()
