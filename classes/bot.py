# from objects.group import Group

import discord

newline = "\n"


class Bot:

    def __init__(self, token: str, group):
        self.token = token
        self.group = group

    async def start(self):

        print("start")

        try:
            print("trying to login bot")
            await self.client.login(token=self.token, bot=True)
        except discord.LoginFailure:
            print("trying to login user")
            # await self.client.close()  # for some reason this code just makes nothing run, i wonder why
            await self.client.login(token=self.token, bot=False)

        await self.client.connect()


