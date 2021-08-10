import tcod

from rgl.renderer import RenderOrder
from rgl.game_states import GameStates

def kill_player(player):
    player.char = '%'
    player.color = tcod.dark_red

    return "You are dead", GameStates.PLAYER_DEATH

def kill_monster(monster):
    death_message = f"{monster.name.capitalize()} is dead!"

    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = f"Remains of {monster.name.capitalize()}"
    monster.render_order = RenderOrder.CORPSE

    return death_message