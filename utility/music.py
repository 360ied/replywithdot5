"""Base Wrapper for the Music Commands"""
import asyncio
import copy
import logging
from collections import deque

import discord

from classes import botexception
from utility import blib

music_queue = list()


# TODO: add clearing of requesters
# TODO: add dj blacklisting


class Piece:
    def __init__(self, name, audio_source_getter, voice_client, text_channel, requester):
        """
        :param str name: Name of the Piece
        :param blib.PreparedCoroutine audio_source_getter: Audio source getter prepared coroutine
        :param discord.VoiceClient voice_client: Associated voice client to play in
        :param discord.TextChannel text_channel: Associated text channel to log in
        :param discord.Member requester: The member who requested the piece
        """
        self.name = name
        self.audio_source = None
        self.audio_source_getter = audio_source_getter
        self.voice_client = voice_client
        self.text_channel = text_channel
        self.requester = requester

    def __str__(self):
        return self.name

    def __copy__(self):
        return Piece(self.name, self.audio_source_getter, self.voice_client, self.text_channel, self.requester)

    async def initialize_audio_source(self):
        logging.debug("initializing audio source")
        self.audio_source = await self.audio_source_getter.run()

    async def play(self):
        """Play the audio source"""
        if self.audio_source is None:
            await self.initialize_audio_source()
            logging.debug("done init audio source")
        logging.debug(self.name)
        logging.debug(self.voice_client)
        logging.debug(type(self.voice_client))
        try:
            self.voice_client.play(self.audio_source)
        except TypeError:
            logging.debug("TypeError")
        logging.debug("IM HERE")
        # await asyncio.sleep(10)
        while self.voice_client.is_playing():
            # logging.info(self.voice_client.is_playing())
            await asyncio.sleep(.1)

    def stop(self):
        """Stop playing the audio source"""
        self.voice_client.stop()

    def pause(self):
        """Pause the playing"""
        self.voice_client.pause()

    def resume(self):
        """Resume the playing"""
        self.voice_client.resume()


class MusicQueue:
    def __init__(self, voice_client, text_channel, pieces=None, looping_current_piece=False, looping_queue=False,
                 current_piece=None):
        """
        :param discord.VoiceClient voice_client: Associated Voice Client
        :param discord.TextChannel text_channel: Associated Text Channel
        :param list pieces: The pieces to queue
        :param bool looping_current_piece: Whether to loop the current piece
        :param bool looping_queue: Whether to loop the queue
        :param Piece current_piece: The current playing piece
        """
        # Avoid mutable default argument
        # Use double-ended queues as they are better as queues than lists
        self.pieces = deque(pieces) if pieces is not None else deque()

        self.looping_current_piece = looping_current_piece
        self.looping_queue = looping_queue
        self.current_piece = current_piece

        self.voice_client = voice_client
        self.text_channel = text_channel

        # self.playing = False

    def add_piece(self, piece):
        """
        :param Piece piece: The piece to add to the queue
        Adds a piece to the end of the queue
        """
        self.pieces.append(piece)

    def add_piece_front(self, piece):
        """
        :param Piece piece: The piece to add to the queue
        Adds a piece to the front of the queue
        """
        self.pieces.appendleft(piece)

    def remove_piece(self, index):
        """
        :param int index: Index of the piece
        :raises IndexError: If the index is invalid
        """
        self.pieces.pop(index)

    def skip_current_piece(self):
        """Skip the current piece"""
        # Stop the current piece
        # Once the current piece is stopped, the next piece will automatically play
        self.current_piece.stop()


    def piece_iterator(self):
        """
        :return: The current piece based on the queue settings
        :rtype: Piece
        Iterate through the pieces in the queue based on the queue settings
        """
        while len(self.pieces) > 0 or self.looping_current_piece:
            logging.info(f"self.pieces is of length {len(self.pieces)}")
            logging.info(str(self.pieces))
            if self.current_piece is None:
                logging.info("Current Piece is None")
                self.current_piece = self.pieces.popleft()
                yield self.current_piece
                continue
            # Looping current piece goes first as it overrides looping the queue
            if self.looping_current_piece:
                # Add a duplicate of the current piece to the front of the queue
                self.add_piece_front(copy.copy(self.current_piece))
                # Then exchange pieces
                self.current_piece = self.pieces.popleft()
            elif self.looping_queue:
                self.current_piece = self.pieces[0]
                # Rotate to the left by 1 to put the current piece at the end of the queue
                self.pieces.rotate(-1)
            else:
                self.current_piece = self.pieces.popleft()

            yield self.current_piece
        logging.warning(f"Exited Generator")

    async def player(self):
        """
        :raises botexception.AlreadyOccupiedException: Already playing the queue
        Plays the queue
        """
        # if self.playing:
        if self.voice_client.is_playing():
            # raise botexception.AlreadyOccupiedException("Already playing the queue")
            logging.info("Already playing the queue")
            return

        for i in self.piece_iterator():
            logging.info(f"Length of self.pieces is {len(self.pieces)}")
            i: Piece
            await self.text_channel.send(f"Now Playing: {i.name}")
            logging.debug("about to play")
            await i.play()

        await self.text_channel.send("Queue is finished.")


class MusicManager:

    def __init__(self, queues=None):
        """
        :param dict queues: Starting queues
        """
        self.queues = queues.copy() if queues is dict else dict()

    async def connect_with_member(self, member, text_channel, timeout=60, reconnect=True):
        """
        :param discord.Member member: Member to join with
        :param discord.TextChannel text_channel: Associated Text Channel
        :param int timeout: Timeout for joining the voice channel
        :param bool reconnect: Whether to reconnect if part of the handshake fails or the gateway goes down
        :return: Music Queue Instance
        :rtype: MusicQueue
        :raises botexception.MemberNotInAnyVoiceChannelException: Member is not in any voice channel, therefore you cannot join them.
        :raises botexception.AlreadyOccupiedException: You are already in a different voice channel.
        :raises asyncio.TimeoutError: Could not connect to the voice channel in time.
        :raises discord.ClientException: You are already connected to a voice channel.
        :raises discord.opus.OpusNotLoaded: The opus library has not been loaded.
        Connect to the same voice channel as a member
        """
        if member.voice is None:
            raise botexception.MemberNotInAnyVoiceChannelException("Member is not in any voice channel")

        self_current_voice_state = member.guild.me.voice
        # Check that we are connected to a channel
        if self_current_voice_state is not None:
            # Check that we are connected to the same channel as the member
            if self_current_voice_state.channel == member.voice.channel:
                try:
                    return self.queues[member.guild.id]
                except KeyError:
                    await member.guild.me.edit(voice_channel=None)
            else:
                raise botexception.AlreadyOccupiedException("I am already in a voice channel")

        voice_client = await blib.connect_with_member(member, timeout=timeout, reconnect=reconnect)

        return self.get_queue(member.guild, voice_client, text_channel)

    def get_queue(self, guild, voice_client, text_channel):
        """
        :param discord.Guild guild: Requesting Guild
        :param discord.VoiceClient voice_client: Voice Client for MusicQueue
        :param discord.TextChannel text_channel: Text Channel for MusicQueue
        :return: Music Queue Instance
        :rtype: MusicQueue

        For getting the queue without a voice client or text channel, call the dictionary directly
        """
        if guild.id not in self.queues:
            self.queues[guild.id] = MusicQueue(voice_client, text_channel)
        return self.queues[guild.id]
