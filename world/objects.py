from ursina import *
import math
import random

spawned = []

# ---------------------------------------------------------
#  PLAY SOUND WHEN OBJECT IS CREATED
# ---------------------------------------------------------
def play_spawn_sound():
    Audio('assets/sounds/pop.wav', autoplay=True)


# ---------------------------------------------------------
#  SPAWN OBJECTS (VISIBLE MODELS)
# ---------------------------------------------------------
def spawn_object(obj, pos, col):
    print("spawn_object() called:", obj, pos, col)

    if obj == "cube":
        e = Entity(model='cube', color=col, position=pos, scale=1)

    elif obj == "sphere":
        e = Entity(model='sphere', color=col, position=pos, scale=1)

    elif obj == "circle":
        e = Entity(model='quad', color=col, position=pos, scale=2)

    elif obj == "smiley":
        draw_smiley(pos)
        play_spawn_sound()
        return

    elif obj == "spiral":
        draw_spiral(pos)
        play_spawn_sound()
        return

    else:
        print("Unknown object:", obj)
        return

    spawned.append(e)
    play_spawn_sound()   # 🔊 SOUND EFFECT HERE


# ---------------------------------------------------------
#  DELETE ALL OBJECTS
# ---------------------------------------------------------
def delete_all_objects():
    print("Deleting all objects...")
    for e in spawned:
        destroy(e)
    spawned.clear()


# ---------------------------------------------------------
#  DRAW SMILEY FACE
# ---------------------------------------------------------
def draw_smiley(center):
    cx, cy, cz = center

    face = Entity(model='quad', color=color.yellow, position=center, scale=4)
    eye1 = Entity(model='sphere', color=color.black, position=(cx - 1, cy + 1, cz), scale=0.3)
    eye2 = Entity(model='sphere', color=color.black, position=(cx + 1, cy + 1, cz), scale=0.3)

    spawned.extend([face, eye1, eye2])
    play_spawn_sound()


# ---------------------------------------------------------
#  DRAW SPIRAL
# ---------------------------------------------------------
def draw_spiral(center):
    cx, cy, cz = center

    for i in range(40):
        angle = i * 0.3
        radius = i * 0.1
        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius

        e = Entity(model='sphere', color=color.random_color(), position=(x, y, cz), scale=0.2)
        spawned.append(e)

    play_spawn_sound()
