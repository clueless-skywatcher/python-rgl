import tcod
import random

from rgl.entity import Entity
from rgl.renderer import RenderOrder
from rgl.map.tile import Tile
from rgl.map.rectangle import RectangleRoom
from rgl.components.ai import BasicMonster
from rgl.components.fighter import Fighter

class GameMap:
    def __init__(self, width, height, entities) -> None:
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.entities = entities
        self.uid = 0

    def initialize_tiles(self):
        tiles = [[Tile(True) for j in range(self.height)] for i in range(self.width)]
        return tiles

    def build_map(self, max_rooms, room_min_size, room_max_size, 
        map_width, map_height, player, entities, max_monsters_per_room
    ):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            w = random.randint(room_min_size, room_max_size)
            h = random.randint(room_min_size, room_max_size)

            x = random.randint(0, map_width - w - 1)
            y = random.randint(0, map_height - h - 1)

            new_room = RectangleRoom(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)

                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    if random.randint(0, 1) == 1:
                        self.create_horizontal_tunnel(prev_x, new_x, prev_y)
                        self.create_vertical_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_vertical_tunnel(prev_y, new_y, prev_x)
                        self.create_horizontal_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, max_monsters_per_room)
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_horizontal_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
    
    def create_vertical_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

    def place_entities(self, room, max_monsters_per_room):
        number_of_monsters = random.randint(0, max_monsters_per_room)
        
        for i in range(number_of_monsters):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in self.entities if entity.x == x and entity.y == y]):
                if random.randint(0, 100) < 80:
                    ai_component = BasicMonster()
                    fighter_component = Fighter(hp = 10, defense = 0, power = 3)
                    monster = Entity(x, y, 'o', tcod.desaturated_green, f"Orc", blocks = True,
                        fighter = fighter_component, ai = ai_component, render_order = RenderOrder.ACTOR)
                else:
                    ai_component = BasicMonster()
                    fighter_component = Fighter(hp = 16, defense = 1, power = 4)
                    monster = Entity(x, y, 'T', tcod.dark_green, f"Troll", blocks = True,
                        fighter = fighter_component, ai = ai_component, render_order = RenderOrder.ACTOR)
                
                self.entities.append(monster)
                self.uid += 1