import sys
import os
import tcod

from rgl.entity import Entity
from rgl.key_handler import InputHandler
from rgl.map.game_map import GameMap
from rgl.renderer import RenderOrder, Renderer
from rgl.death_funcs import kill_monster, kill_player
from rgl.fov_funcs import initialize_fov, recompute_fov
from rgl.game_states import GameStates
from rgl.components.fighter import Fighter
from rgl.components.ai import BasicMonster

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

        self.fov_algorithm = 0
        self.fov_light_walls = True
        self.fov_radius = 5

        self.max_monsters_per_room = 3

        self.COLORS = {
            "DarkWall": tcod.Color(0, 0, 100),
            "DarkGround": tcod.Color(50, 50, 150),
            "LightWall": tcod.Color(130, 110, 50),
            "LightGround": tcod.Color(200, 180, 50)
        }

        self.fov_recompute = True        

        self.fighter_component = Fighter(hp = 30, defense = 2, power = 5)
        self.player_entity = Entity(int(self.scr_width / 2), int(self.scr_height / 2), self.player_symbol, tcod.white, "Player", blocks = True, fighter = self.fighter_component, render_order = RenderOrder.ACTOR)
        self.entities = [self.player_entity]

        self.game_map = GameMap(map_width, map_height, self.entities)
        self.game_map.build_map(max_rooms, room_min_size, room_max_size, map_width, map_height, self.player_entity, self.entities, self.max_monsters_per_room)

    def run(self):
        tcod.console_set_custom_font('assets/arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        tcod.console_init_root(self.scr_width, self.scr_height, self.scr_title, False)
        console = tcod.console_new(self.scr_width, self.scr_height)
        
        key = tcod.Key()
        mouse = tcod.Mouse()

        fov_map = initialize_fov(self.game_map)

        game_state = GameStates.PLAYER_TURN

        renderer = Renderer(console, self.entities, self.player_entity, self.game_map, fov_map, True)
        while not tcod.console_is_window_closed():
            if self.fov_recompute:
                recompute_fov(fov_map, self.player_entity.x, self.player_entity.y, self.fov_radius, self.fov_light_walls, self.fov_algorithm)
            tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
            renderer.render_all(self.scr_width, self.scr_height, self.COLORS)
            tcod.console_flush()

            renderer.clear_all()

            key_handler = InputHandler()
            move = key_handler.handle_key(key).get("move")
            exit = key_handler.handle_key(key).get("exit")
            fullscreen = key_handler.handle_key(key).get("fullscreen")

            player_turn_results = []

            if move and game_state == GameStates.PLAYER_TURN:
                dx, dy = move
                if not self.game_map.is_blocked(self.player_entity.x + dx, self.player_entity.y + dy):
                    dest_x = self.player_entity.x + dx
                    dest_y = self.player_entity.y + dy
                    target = self.player_entity.get_all_blocking_entities_at_location(self.entities, dest_x, dest_y)
                    if target:
                        attack = self.player_entity.fighter.attack(target)
                        player_turn_results.extend(attack)
                    else:
                        self.fov_recompute = True
                        self.player_entity.move(dx, dy)

                game_state = GameStates.ENEMY_TURN

            if exit:
                return True

            if fullscreen:
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

            for result in player_turn_results:
                message = result.get("message")
                dead_entity = result.get("dead")

                if message:
                    print(message)
                if dead_entity:
                    if dead == self.player_entity:
                        message, game_state = kill_player(dead_entity)
                    else:
                        message = kill_monster(dead_entity)

                    print(message)

            if game_state == GameStates.ENEMY_TURN:
                for entity in self.entities:
                    if entity.ai and fov_map.fov[entity.y][entity.x]:
                        enemy_turn_results = entity.ai.take_turn(self.player_entity, fov_map, self.game_map, self.entities)
                        for result in enemy_turn_results:
                            message = result.get("message")
                            dead = result.get("dead")

                            if message:
                                print(message)
                            
                            if dead:
                                if dead == self.player_entity:
                                    message, game_state = kill_player(dead)
                                else:
                                    message = kill_monster(dead)

                                print(message)

                            if game_state == GameStates.PLAYER_DEATH:
                                break

                        if game_state == GameStates.PLAYER_DEATH:
                            break
                        
                else:
                    game_state = GameStates.PLAYER_TURN

if __name__ == '__main__':
    game = MainScript(80, 50, 80, 45)
    game.run()