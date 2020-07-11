import discord

from utility import blib


class ExtendedMember:

    def __init__(self, member: discord.Member):
        self.member: discord.Member = member
        self.trust_score = None

    def get_trust_score(self):
        pass
