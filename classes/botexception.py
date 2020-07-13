class BotException(Exception):
    pass


class MissingPermissionsException(BotException):
    pass


class MemberNotInAnyVoiceChannelException(BotException):
    pass


class AlreadyOccupiedException(BotException):
    pass
