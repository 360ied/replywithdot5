from utility.blib import WrappedTuple

emotes_list = ["⏪", "◀️", "▶️", "⏩"]


class Menu:
    """Discord Reaction Menu"""

    def __init__(self, me, channel, pages, menu_manager, operator_check=lambda x: True, current_index=0, message=None):
        """
        :param discord.User me:
        :param discord.TextChannel channel:
        :param pages: iterable of embeds, or just one embed if you want automatic splitting
        :param MenuManager menu_manager:
        :param operator_check: A function taking one argument of discord.Member and returning a boolean
        :param int current_index: The current index of the menu
        :param discord.Message message:
        """
        self.me = me
        self.channel = channel
        self.message = message
        self.pages = WrappedTuple(pages)
        self.menu_manager = menu_manager
        self.current_index = current_index
        self.operator_check = operator_check

        self.emote_to_func = {
            "⏪": self.recede_page_to_start,
            "◀️": self.recede_page,
            "▶️": self.advance_page,
            "⏩": self.advance_page_to_end
        }

    async def send(self):
        self.message = await self.channel.send(embed=self.pages[self.current_index])
        self.menu_manager.register_menu(self)
        await self.add_reaction_menu()

    async def add_reaction_menu(self):
        for i in emotes_list:
            await self.message.add_reaction(i)

    async def remove_other_reactions(self):
        for i in self.message.reactions:
            async for ii in i.users():
                if not self.me.id == ii.id:
                    await i.remove(ii)

    async def set_page(self, index):
        await self.message.edit(embed=self.pages[index])
        self.current_index = index
        await self.remove_other_reactions()

    async def advance_page(self, n=1):
        self.current_index += n
        await self.set_page(self.current_index)

    async def recede_page(self, n=1):
        await self.advance_page(-n)

    async def advance_page_to_end(self):
        await self.set_page(len(self.pages) - 1)

    async def recede_page_to_start(self):
        await self.set_page(0)


class MenuManager:
    """Allows for updating of menus from reactions"""

    def __init__(self, menus=None):
        self.menu_getter = {menu.message.id: menu for menu in (list(menus) if menus is not None else list())}

    def register_menu(self, menu):
        self.menu_getter[menu.message.id] = menu

    async def on_reaction_add(self, client, raw_reaction_action_event):
        """
        :param discord.Client client:
        :param discord.RawReactionActionEvent raw_reaction_action_event:
        Applies menu changes upon event
        """
        if raw_reaction_action_event.member.id == client.user.id:
            return
        if raw_reaction_action_event.message_id in self.menu_getter:
            if str(raw_reaction_action_event.emoji) in emotes_list:
                menu = self.menu_getter[raw_reaction_action_event.message_id]
                if menu.operator_check(raw_reaction_action_event.member):
                    await menu.emote_to_func[str(raw_reaction_action_event.emoji)]()
