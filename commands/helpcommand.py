"""Help Command"""
import discord

description = __doc__

usage = "{prefix}help [command]"

aliases = {
    "command": "command"
}

required_parameters = set()

required_permissions = set()

expected_positional_parameters = [
    "command"
]


async def run(client: discord.Client, group, message: discord.Message, args: dict) -> None:
    guild_prefix = await client.get_prefix_of_guild(message.guild)
    if "command" in args:
        command_name = args["command"].lower()
        try:
            command = client.command_dict[command_name]
        except KeyError:
            await message.channel.send(f"Unknown command `{command_name}`")
        else:
            embed = discord.Embed(
                title=command.description,
                description=command.usage.replace("{prefix}", guild_prefix)
            )
            embed.set_footer(text=f"Requested by {str(message.author)}")
            await message.channel.send(embed=embed)
    else:
        commands = client.command_dict.keys()
        command_names = [f"`{guild_prefix}{x}`" for x in commands]
        commands_str = f"{len(commands)} commands\n" \
                       f"{','.join(command_names)}"
        embed = discord.Embed(
            title="Help Command",
            description=commands_str
        )
        embed.set_footer(text=f"Requested by {str(message.author)}")
        await message.channel.send(embed=embed)
