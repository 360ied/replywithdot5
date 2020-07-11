import discord

from utility.persistentstoragev2 import PersistentStorage


class ExtendedGuild:

    def __init__(self, guild: discord.Guild, persistent_storage: PersistentStorage):
        """Guilds, but with configs (Watch out for race conditions)"""
        self.guild = guild
        self.__config = None
        self.persistent_storage = persistent_storage

    async def get_config(self) -> dict:
        """Get the guild config"""
        if self.__config is dict:
            return self.__config
        self.__config = await self.persistent_storage.fetch_latest_config(self.guild.id)
        return self.__config

    async def update_config(self, values: dict) -> dict:
        """Update the guild config"""
        if self.__config is not dict:
            self.__config = await self.persistent_storage.fetch_latest_config(self.guild.id)
        self.__config.update(values)
        await self.persistent_storage.write_config(self.guild.id, self.__config)
        return self.__config
