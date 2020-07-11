from classes.bot import Bot

from classes.bots.type1 import Type1

from utility import blib


class Group:
    """This is supposed to act like a 'SuperClient' of multiple accounts"""

    def __init__(self):
        # Create bot dictionary to store all instances
        self.bots = dict()

        # Set containing the types of derivatives of objects.bots.bot.Bot
        self.bot_types = {Type1}

        self.bot_type_dict = {
            bot_type.__name__: bot_type for bot_type in self.bot_types
        }

        # Creates a category set for each bot type
        for bot_type in self.bot_types:
            self.bots[bot_type] = set()

    def load_bot_config(self, bot_config: dict) -> None:
        """Loads all valid bot types from a dict"""
        for key, value in bot_config.items():
            bot_type = self.bot_type_dict[key]
            self.add_bots({
                bot_type(x, self) for x in value
            })

    def add_bots(self, bots) -> None:
        """Adds an iterable of bots (can be of mixed type) to the Group"""
        for i in bots:
            self.add_bot(i)

    def add_bot(self, bot: Bot) -> None:
        """Adds a bot to the correct type in the Group"""
        self.bots[type(bot)].add(bot)

    def remove_bots(self, bots: set) -> None:
        """Removes an iterable of bots (can be of mixed type) from the Group"""
        for i in bots:
            self.remove_bot(i)

    def remove_bot(self, bot: Bot) -> None:
        """Removes a bot from the Group"""
        self.bots[type(bot)].remove(bot)

    def get_bot_list(self) -> set:
        """Returns a flattened set of all bots"""
        return {
            xx for x in self.bots.items() for xx in x[1]  # x[1] is the value of the key, value pair
        }

    # :sunglasses:

    def super_call(self, attribute: str, bot_types: set) -> object:
        """Tries to find a non-nonetype value by iterating through bots"""
        for type_ in bot_types:
            for bot in self.bots[type_]:
                client = bot.client
                returned = getattr(client, attribute)
                if returned is None:
                    continue
                return returned

    def super_call_func(self, attribute: str, bot_types: set, args=None, if_map=blib.return_true) -> tuple:
        """Returns 2 values, the returned value and the client which was used to get the value"""
        if args is None:
            args = []
        for type_ in bot_types:
            for bot in self.bots[type_]:
                if if_map(client=bot.client):
                    client = bot.client
                else:
                    continue
                returned = getattr(client, attribute)(*args)
                if returned is None:
                    continue
                return returned, client
        return None, None

    def super_call_all(self, attribute: str, bot_types: set):
        """Returns all values"""
        to_return = set()
        # clients = set()
        for type_ in bot_types:
            for bot in self.bots[type_]:
                client = bot.client
                returned = getattr(client, attribute)
                if returned is None:
                    continue
                to_return.update(returned)
                # clients.add(client)

        return to_return
