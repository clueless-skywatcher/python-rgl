import math
import tcod

from rgl.renderer import RenderOrder

class Entity:
    def __init__(self, x, y, 
        char, 
        color, 
        name, 
        blocks = False,
        fighter = None,
        ai = None,
        render_order = RenderOrder.CORPSE
    ) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fighter = fighter
        self.ai = ai
        self.render_order = render_order

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_all_blocking_entities_at_location(self, entities, dest_x, dest_y):
        for entity in entities:
            if entity.blocks and entity.x == dest_x and entity.y == dest_y:
                return entity
        
        return None

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or 
            self.get_all_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def move_astar(self, target, entities, game_map):
        fov = tcod.map_new(game_map.width, game_map.height)

        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                fov.transparent[y1][x1] = not game_map.tiles[x1][y1].block_sight
                fov.walkable[y1][x1] = not game_map.tiles[x1][y1].blocked

        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                fov.transparent[entity.y][entity.x] = True
                fov.walkable[entity.y][entity.x] = False

        path = tcod.path_new_using_map(fov, 1.41)
        
        tcod.path_compute(path, self.x, self.y, target.x, target.y)

        if not tcod.path_is_empty(path) and tcod.path_size(path) < 25:
            x, y = tcod.path_walk(path, True)
            if x or y:
                self.x = x
                self.y = y
        else:
            self.move_towards(target.x, target.y, game_map, entities)
        
        tcod.path_delete(path)

    