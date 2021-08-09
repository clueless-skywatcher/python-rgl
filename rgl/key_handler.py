import tcod

class InputHandler:
    def __init__(self) -> None:
        self.__dict = {}

    def handle_key(self, key):
        if key.vk == tcod.KEY_UP:
            self.__dict = {"move": (0, -1)}
        elif key.vk == tcod.KEY_DOWN:
            self.__dict = {"move": (0, 1)}
        elif key.vk == tcod.KEY_LEFT:
            self.__dict = {"move": (-1, 0)}
        elif key.vk == tcod.KEY_RIGHT:
            self.__dict = {"move": (1, 0)}

        if key.vk == tcod.KEY_ENTER and key.lalt:
            self.__dict = {"fullscreen": True}
        elif key.vk == tcod.KEY_ESCAPE:
            self.__dict = {"exit": True}

        return self.__dict

