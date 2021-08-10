from numpy.core.fromnumeric import sort
import tcod
from enum import Enum

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

class Renderer:
    def __init__(self, console, entities, player, game_map, fov_map, fov_recompute) -> None:
        self.console = console
        self.entities = entities
        self.player = player
        self.game_map = game_map
        self.fov_map = fov_map
        self.fov_recompute = fov_recompute

    def render_all(self, width, height, render_color_dict):
        if self.fov_recompute:
            for y in range(self.game_map.height):
                for x in range(self.game_map.width):
                    visible = self.fov_map.fov[y][x]
                    wall = self.game_map.tiles[x][y].block_sight
                    if visible:
                        if wall:
                            tcod.console_set_char_background(self.console, 
                                x, y, render_color_dict.get("LightWall"), tcod.BKGND_SET)
                        else:
                            tcod.console_set_char_background(self.console, 
                                x, y, render_color_dict.get("LightGround"), tcod.BKGND_SET)
                        self.game_map.tiles[x][y].explored = True
                    elif self.game_map.tiles[x][y].explored:
                        if wall:
                            tcod.console_set_char_background(self.console, 
                                x, y, render_color_dict.get("DarkWall"), tcod.BKGND_SET)
                        else:
                            tcod.console_set_char_background(self.console, 
                                x, y, render_color_dict.get("DarkGround"), tcod.BKGND_SET)

        self.entities = sorted(self.entities, key = lambda x: x.render_order.value)

        for entity in self.entities:
            if self.fov_map.fov[entity.y][entity.x]:
                self.draw_entity(entity)

        tcod.console_set_default_foreground(self.console, tcod.white)
        tcod.console_print_ex(self.console, 1, height - 2, tcod.BKGND_NONE, tcod.LEFT, f"HP: {self.player.fighter.hp:02}/{self.player.fighter.max_hp:02}")

        tcod.console_blit(self.console, 0, 0, width, height, 0, 0, 0)

    def draw_entity(self, entity):
        tcod.console_set_default_foreground(self.console, entity.color)
        tcod.console_put_char(self.console, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

    def clear_entity(self, entity):
        tcod.console_put_char(self.console, entity.x, entity.y, ' ', tcod.BKGND_NONE)

    def clear_all(self):
        for entity in self.entities:
            self.clear_entity(entity)