import sys
import os
import tcod

from rgl.key_handler import InputHandler

os.environ['path'] = f"{os.path.dirname(sys.executable)};{os.environ['path']}"

import glob

class MainScript():
    def __init__(self, scr_width, scr_height, player_symbol = '@', scr_title = 'RGL') -> None:
        self.scr_width = scr_width
        self.scr_height = scr_height
        self.scr_title = scr_title
        self.player_symbol = player_symbol

        self.player_x = int(self.scr_width / 2)
        self.player_y = int(self.scr_height / 2)

    def run(self):
        tcod.console_set_custom_font('assets/arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        tcod.console_init_root(self.scr_width, self.scr_height, self.scr_title, False)
        console = tcod.console_new(self.scr_width, self.scr_height)
        
        key = tcod.Key()
        mouse = tcod.Mouse()

        while not tcod.console_is_window_closed():
            tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
            tcod.console_set_default_foreground(console, tcod.white)
            tcod.console_put_char(console, self.player_x, self.player_y, self.player_symbol, tcod.BKGND_NONE)
            tcod.console_blit(console, 0, 0, self.scr_width, self.scr_height, 0, 0, 0)
            tcod.console_flush()

            tcod.console_put_char(console, self.player_x, self.player_y, ' ', tcod.BKGND_NONE)

            key_handler = InputHandler()
            move = key_handler.handle_key(key).get("move")
            exit = key_handler.handle_key(key).get("exit")
            fullscreen = key_handler.handle_key(key).get("fullscreen")

            if move:
                dx, dy = move
                self.player_x += dx
                self.player_y += dy

            if exit:
                return True

            if fullscreen:
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

if __name__ == '__main__':
    game = MainScript(80, 50)
    game.run()