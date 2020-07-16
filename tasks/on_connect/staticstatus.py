import discord


async def run(client: discord.Client, status: str):
    await client.change_presence(
        activity=discord.Activity(
            name=status,
            type=0
        )
    )
