
import sys
import os
import tcod

from rgl.entity import Entity
from rgl.key_handler import InputHandler
from rgl.map.game_map import GameMap
from rgl.renderer import Renderer

os.environ['path'] = f"{os.path.dirname(sys.executable)};{os.environ['path']}"

import glob

class MainScript():
    def __init__(self, scr_width, scr_height, map_width, map_height, 
        player_symbol = '@', 
        scr_title = 'RGL', 
        max_rooms = 30, 
        room_min_size = 6,
        room_max_size = 10
    ) -> None:
        self.scr_width = scr_width
        self.scr_height = scr_height
        self.scr_title = scr_title
        self.player_symbol = player_symbol
        
        self.map_width = map_width
        self.map_height = map_height

        self.max_rooms = max_rooms
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size

        self.COLORS = {
            "DarkWall": tcod.Color(0, 0, 100),
            "DarkGround": tcod.Color(50, 50, 150)
        }

        self.game_map = GameMap(map_width, map_height)

        self.player_entity = Entity(int(self.scr_width / 2), int(self.scr_height / 2), self.player_symbol, tcod.white)
        npc_entity = Entity(int(self.scr_width / 2 - 5), int(self.scr_height / 2 - 5), 'g', tcod.yellow)

        self.entities = [self.player_entity, npc_entity]
        self.game_map.build_map(max_rooms, room_min_size, room_max_size, map_width, map_height, self.player_entity)

    def run(self):
        tcod.console_set_custom_font('assets/arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        tcod.console_init_root(self.scr_width, self.scr_height, self.scr_title, False)
        console = tcod.console_new(self.scr_width, self.scr_height)
        
        key = tcod.Key()
        mouse = tcod.Mouse()
        renderer = Renderer(console, self.entities, self.game_map)

        while not tcod.console_is_window_closed():
            tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
            # tcod.console_set_default_foreground(console, tcod.white)
            # tcod.console_put_char(console, self.player_entity.x, self.player_entity.y, self.player_symbol, tcod.BKGND_NONE)
            # tcod.console_blit(console, 0, 0, self.scr_width, self.scr_height, 0, 0, 0)
            renderer.render_all(self.scr_width, self.scr_height, self.COLORS)
            tcod.console_flush()

            # tcod.console_put_char(console, self.player_entity.x, self.player_entity.y, ' ', tcod.BKGND_NONE)
            renderer.clear_all()

            key_handler = InputHandler()
            move = key_handler.handle_key(key).get("move")
            exit = key_handler.handle_key(key).get("exit")
            fullscreen = key_handler.handle_key(key).get("fullscreen")

            if move:
                dx, dy = move
                if not self.game_map.is_blocked(self.player_entity.x + dx, self.player_entity.y + dy):
                    self.player_entity.move(dx, dy)

            if exit:
                return True

            if fullscreen:
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

if __name__ == '__main__':
    game = MainScript(80, 50, 80, 45)
    game.run()