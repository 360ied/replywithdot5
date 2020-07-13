"""Persistent Storage V2"""
import json
from io import StringIO

import discord


async def fetch_latest_message(text_channel: discord.TextChannel) -> discord.Message:
    """Gets the latest message in a text channel"""
    return (await text_channel.history(limit=1).flatten())[0]


class PersistentStorage:

    def __init__(self, host_guild: discord.Guild):
        """
        Using Discord as a storage format!
        Allows storage of json files using Discord
        """
        self.host_guild: discord.Guild = host_guild
        self.config_cache = dict()

    async def get_channel(self, guild_id: int) -> discord.TextChannel:
        """Returns the config channel for a guild"""
        for i in self.host_guild.text_channels:
            if str(i) == str(guild_id):
                return i
        # No channel has been found, so create a new one
        channel = await self.host_guild.create_text_channel(str(guild_id))
        await channel.send(file=discord.File(StringIO("{}"), filename=f"{guild_id}.json"))

    async def fetch_latest_config(self, guild_id: int) -> dict:
        """Gets the latest config for a guild in dict format"""
        return json.loads(
            (await (
                await fetch_latest_message(
                    await self.get_channel(guild_id))).attachments[0].read()).decode("utf-8"))

    async def write_config(self, guild_id: int, config: dict) -> str:
        """Writes a config for a guild and returns the url of the config"""
        return (await (await self.get_channel(guild_id)).send(
            file=discord.File(StringIO(json.dumps(config)), filename=f"{guild_id}.json"))).attachments[0].url

    async def get_config(self, guild_id: int) -> dict:
        """Use this instead of fetch latest config"""
        if guild_id not in self.config_cache:
            print(f"{guild_id} not in {self.config_cache}")
            self.config_cache[guild_id] = await self.fetch_latest_config(guild_id)
        return self.config_cache[guild_id]

    async def update_config(self, guild_id: int, config: dict) -> dict:
        """Config dict does not have to be complete"""
        if guild_id not in self.config_cache:
            self.config_cache[guild_id] = await self.fetch_latest_config(guild_id)
        self.config_cache[guild_id].update(config)
        return self.config_cache[guild_id]

    async def write_config_cache(self) -> list:
        """Returns the file URLs"""
        return [await self.write_config(k, v) for k, v in self.config_cache.items()]
