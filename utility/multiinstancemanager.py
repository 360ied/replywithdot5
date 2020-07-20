import logging
from asyncio import sleep
from getpass import getuser
from os import getenv
from time import time

from utility.blib import fetch_latest_message, get_snowflake_epoch

username = getuser()


class MultiInstanceManager:

    def __init__(
            self,
            client,
            status_channel_id=int(getenv("status_channel_id")),
            timeout_seconds=10,
            retry_seconds=15,
            status_seconds=5
    ):
        """
        :param discord.Client client:
        :param int status_channel_id:
        :param int timeout_seconds:
        :param int retry_seconds:
        :param int status_seconds:
        """

        self.client = client
        self.status_channel_id = status_channel_id
        self.timeout_seconds = timeout_seconds
        self.retry_seconds = retry_seconds
        self.status_seconds = status_seconds
        self.enabled = False
        self.status_channel = self.client.get_channel(self.status_channel_id)

    async def am_i_only_instance(self):
        latest_message = await fetch_latest_message(self.status_channel)
        latest_message_epoch = get_snowflake_epoch(latest_message.id)

        current_time = int(time())
        if current_time - latest_message_epoch > self.timeout_seconds:
            await self.status_channel.send(f"{current_time} - {latest_message_epoch} > {self.timeout_seconds}")
            return True
        else:
            return False

    async def checker(self):
        """
        Waits until you are the only instance running
        """
        while True:
            if await self.am_i_only_instance():
                self.enabled = True
                logging.info(f"Enabled!")
                self.client.loop.create_task(self.claimer())
                return True
            logging.info("There are other instances running.")
            await sleep(self.retry_seconds)

    async def claimer(self):
        while True:
            await self.status_channel.send(username)
            await sleep(self.status_channel)
