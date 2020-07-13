import asyncio
import json
import logging
import os
import sys

import discord

import keepalive
from classes.group import Group

keepalive.keep_alive()
logging.basicConfig(level=logging.INFO)

# For FFmpeg support
sys.path.append("./libraries/")

# Allow for playing of audio
discord.opus.load_opus("./libraries/libopus.so.0.8.0")

group = Group()

config = json.loads(os.environ.get("config"))

group.load_bot_config(config["bots"])

loop = asyncio.get_event_loop()

for bot in group.get_bot_list():
    loop.create_task(bot.start())

loop.run_forever()

print("Started")
