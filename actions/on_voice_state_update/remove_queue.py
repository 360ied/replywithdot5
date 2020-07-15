"""Removes unnecessary queues from the music manager"""

import logging

import discord

from utility import music


async def run(client: discord.Client, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if client.user.id == member.id:
        if after.channel is None:
            music_manager: music.MusicManager = client.music_manager
            del music_manager.queues[member.guild.id]
            logging.info(f"Removed queue from {str(member.guild)}")
