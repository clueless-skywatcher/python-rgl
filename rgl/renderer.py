import tcod

class Renderer:
    def __init__(self, console, entities) -> None:
        self.console = console
        self.entities = entities

    def render_all(self, width, height):
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