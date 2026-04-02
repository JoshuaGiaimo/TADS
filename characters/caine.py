from ursina import *
import random
import time
import threading
from ai.speech_queue import speak_cain

def create_caine():
    cain = Entity(model='cube', color=color.red, scale=1.5, position=(0, 1, 0))
    cain.target = cain.position

    # Fake cylinder hat (cube stretched)
    Entity(
        parent=cain,
        model='cube',
        color=color.black,
        scale=(0.6, 1.0, 0.6),
        position=(0, 1.1, 0)
    )

    Entity(
        parent=cain,
        model='cube',
        color=color.black,
        scale=(1.6, 0.1, 1.6),
        position=(0, 0.85, 0)
    )

    return cain


def update_caine(cain):
    cain.position = lerp(cain.position, cain.target, 4 * time.dt)


def start_caine_autonomy(cain):
    def loop():
        while True:
            time.sleep(random.uniform(3, 7))

            # NO MORE TOP HAT LINE
            # Cain just wanders silently unless YOU talk to him.

            cain.target = Vec3(
                random.uniform(-5, 5),
                1,
                random.uniform(-5, 5)
            )

    threading.Thread(target=loop, daemon=True).start()


def extract_field(text, field):
    tag = field.upper() + ":"
    if tag not in text:
        return ""
    part = text.split(tag, 1)[1]
    for other in ["SAY:", "ACTION:", "OBJECT:", "POSITION:", "COLOR:", "CODE:"]:
        if other in part and other != tag:
            part = part.split(other)[0]
    return part.strip()


def parse_color(col):
    if not col:
        return color.white
    col = col.lower()
    if hasattr(color, col):
        return getattr(color, col)
    return color.white


def parse_position(pos):
    try:
        x, y, z = pos.split(",")
        return float(x), float(y), float(z)
    except:
        return 0, 1, 0
