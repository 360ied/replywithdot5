import traceback
from os import environ

import discord

# from actions.on_message import
from actions.on_raw_reaction_add import reactionroleassigner
from actions.on_voice_state_update import remove_queue
from classes.bot import Bot
from tasks.on_connect import staticstatus, persistentstorageautoupdate
from utility import blib
from utility.music import MusicManager
from utility.persistentstoragev2 import PersistentStorage


class Type1(Bot):

    def __init__(self, token: str, group):
        super().__init__(token, group)

        class Client(discord.Client):

            def __init__(self, loop=None, **options):
                super().__init__(loop=loop, **options)
                self.persistent_storage = None
                self.command_dict = None
                self.music_manager = MusicManager()

            async def on_connect(self):
                self.command_dict = command_dict
                self.persistent_storage = PersistentStorage(self.get_guild(int(environ.get("host_guild_id"))))
                for i in task_dict["on_connect"]:
                    self.loop.create_task(i)

            async def get_prefix_of_guild(self, guild):
                try:
                    return (await self.persistent_storage.get_config(guild.id))["prefix"]
                except KeyError:
                    return default_prefix

            async def on_message(self, message):
                for i in actions_dict["on_message"]:
                    self.loop.create_task(i.run(self, message))
                # if message.content.startswith(prefix):
                prefix = await self.get_prefix_of_guild(message.guild)
                # Due to the presence of return statements, this should always be last.
                if message.content.startswith(prefix):
                    prefix_and_command = message.content.split(string_separator)[0]
                    try:
                        # Dictionaries are O(1), while iterating through a list is O(n/2)
                        # Identify Command
                        command = command_dict[prefix_and_command[len(prefix):]]
                    except KeyError:
                        # Command not found
                        return
                    else:
                        # Command found
                        # Check for permissions
                        for i in command.required_permissions:
                            if not getattr(message.author.guild_permissions, i) is True:
                                await message.channel.send(f"Lacking Required Permissions!\n"
                                                           f"You are missing the permission {i}")
                                return

                        argument_string = message.content[len(prefix_and_command) + 1:]

                        command_arguments = blib.command_argument_parser(
                            argument_string, command.expected_positional_parameters
                        )
                        # Map arguments from their aliases
                        mapped_arguments = blib.map_aliases(
                            command_arguments,
                            command.aliases
                        )
                        # Check if all the required parameters are present
                        if not len(set(mapped_arguments.keys()) & command.required_parameters) == len(
                                command.required_parameters):
                            await message.channel.send(f"Lacking Required Parameters!\n"
                                                       f"You are missing the parameters:\n"
                                                       f"{', '.join(command.required_parameters)}")
                            return

                        async with message.channel.typing():
                            try:
                                await command.run(self, group, message, mapped_arguments)
                            except Exception as e:
                                traceback.print_exc()
                                await message.channel.send(f"{type(e).__name__}: {str(e)}")

            async def on_raw_reaction_add(self, payload):
                for i in actions_dict["on_raw_reaction_add"]:
                    self.loop.create_task(i.run(self, payload))

            async def on_voice_state_update(self, member, before, after):
                for i in actions_dict["on_voice_state_update"]:
                    self.loop.create_task(i.run(self, member, before, after))

        self.client = Client()

        task_dict = {
            "on_connect": [
                staticstatus.run(self.client, "New Music Commands! (In Heavy Development)"),
                persistentstorageautoupdate.run(self.client)
            ]
        }

        default_prefix = ","

        # Commands are imported here to create separate instances for each bot
        from commands import ping, setprefix, helpcommand, wolframalpha, meaning, addreactionrole, \
            musicplay, musicloop, musicskip, musicdisconnect, musicnowplaying, musicloopqueue, musicviewqueue, \
            musicremove, musicpause, musicresume

        # Sort the dictionary alphabetically by the key
        command_dict = dict(
            sorted(
                {
                    "ping": ping,
                    "prefix": setprefix,
                    "setprefix": setprefix,
                    "changeprefix": setprefix,
                    "help": helpcommand,
                    "wolfram": wolframalpha,
                    "wr": wolframalpha,
                    "meaning": meaning,
                    "definition": meaning,
                    "mn": meaning,
                    "df": meaning,
                    "addreactionrole": addreactionrole,
                    "arr": addreactionrole,
                    "play": musicplay,
                    "p": musicplay,
                    "loop": musicloop,
                    "skip": musicskip,
                    "disconnect": musicdisconnect,
                    "dc": musicdisconnect,
                    "nowplaying": musicnowplaying,
                    "np": musicnowplaying,
                    "loopqueue": musicloopqueue,
                    "queue": musicviewqueue,
                    "q": musicviewqueue,
                    "remove": musicremove,
                    "r": musicremove,
                    "pause": musicpause,
                    "resume": musicresume
                }.items(), key=lambda item: item[0]))

        actions_dict = {
            "on_message": {
            },
            "on_raw_reaction_add": {
                reactionroleassigner
            },
            "on_voice_state_update": {
                remove_queue
            }
        }

        string_separator = " "
