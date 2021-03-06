import tcod

class InputHandler:
    def __init__(self) -> None:
        self.__dict = {}

    def handle_key(self, key):
        if key.vk == tcod.KEY_UP or key.vk == tcod.KEY_KP8:
            self.__dict = {"move": (0, -1)}
        elif key.vk == tcod.KEY_DOWN or key.vk == tcod.KEY_KP2 or key.vk == tcod.KEY_KP5:
            self.__dict = {"move": (0, 1)}
        elif key.vk == tcod.KEY_LEFT or key.vk == tcod.KEY_KP4:
            self.__dict = {"move": (-1, 0)}
        elif key.vk == tcod.KEY_RIGHT or key.vk == tcod.KEY_KP6:
            self.__dict = {"move": (1, 0)}
        elif key.vk == tcod.KEY_KP7:
            self.__dict = {"move": (-1, -1)}
        elif key.vk == tcod.KEY_KP9:
            self.__dict = {"move": (1, -1)}
        elif key.vk == tcod.KEY_KP1:
            self.__dict = {"move": (-1, 1)}
        elif key.vk == tcod.KEY_KP3:
            self.__dict = {"move": (1, 1)}
        
        if key.vk == tcod.KEY_ENTER and key.lalt:
            self.__dict = {"fullscreen": True}
        elif key.vk == tcod.KEY_ESCAPE:
            self.__dict = {"exit": True}

        return self.__dict

