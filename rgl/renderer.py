import tcod

class Renderer:
    def __init__(self, console, entities, game_map) -> None:
        self.console = console
        self.entities = entities
        self.game_map = game_map

    def render_all(self, width, height, render_color_dict):
        for y in range(self.game_map.height):
            for x in range(self.game_map.width):
                wall = self.game_map.tiles[x][y].block_sight
                if wall:
                    tcod.console_set_char_background(self.console, 
                        x, y, render_color_dict.get("DarkWall"), tcod.BKGND_SET)
                else:
                    tcod.console_set_char_background(self.console, 
                        x, y, render_color_dict.get("DarkGround"), tcod.BKGND_SET)


        for entity in self.entities:
            self.draw_entity(entity)

        tcod.console_blit(self.console, 0, 0, width, height, 0, 0, 0)

    def draw_entity(self, entity):
        tcod.console_set_default_foreground(self.console, entity.color)
        tcod.console_put_char(self.console, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

    def clear_entity(self, entity):
        tcod.console_put_char(self.console, entity.x, entity.y, ' ', tcod.BKGND_NONE)

    def clear_all(self):
        for entity in self.entities:
            self.clear_entity(entity)