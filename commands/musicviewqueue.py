"""Shows the queue"""
import discord

from utility import music
from utility.music import MusicQueue
from utility.menu import Menu

description = __doc__

usage = "{prefix}queue\n"

aliases = dict()

required_parameters = set()

required_permissions = set()

expected_positional_parameters = list()


async def run(client: discord.Client, group, message: discord.Message, args: dict):
    # noinspection PyUnresolvedReferences
    music_manager: music.MusicManager = client.music_manager

    try:
        queue: MusicQueue = music_manager.queues[message.guild.id]
    except KeyError:
        await message.channel.send("There is nothing playing!")
        return "There is nothing playing!"

    parts = list()

    embed = discord.Embed()
    embed.title = f"Current Piece: {queue.current_piece.embed.title} - Requested By {str(queue.current_piece.requester)}"
    embed.set_footer(text=f"Requested by {str(message.author)}", icon_url=str(message.author.avatar_url))
    for c, i in enumerate(queue.pieces):
        i: music.Piece
        if len(embed.copy().add_field(
            name=f"{c + 1}:",
            value=f"{i.embed.title} - Requested By {str(i.requester)}",
            inline=False
        )) > 6000:
            parts.append(embed)

            embed = discord.Embed()
            embed.title = f"Current Piece: {queue.current_piece.embed.title} - Requested By {str(queue.current_piece.requester)} - Part {len(parts)}"
            embed.set_footer(text=f"Requested by {str(message.author)}", icon_url=str(message.author.avatar_url))
        else:
            embed.add_field(
                name=f"{c + 1}:",
                value=f"{i.embed.title} - Requested By {str(i.requester)}",
                inline=False
            )

    parts.append(embed)

    # Send the menu
    # noinspection PyUnresolvedReferences
    await Menu(client.user, message.channel, parts, client.menu_manager).send()
