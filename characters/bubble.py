from ursina import *
import random
import time
import threading
from ai.speech_queue import speak_bubble

def create_bubble(cain):
    bubble = Entity(model='sphere', color=color.azure, scale=0.8, position=(2, 2, 0))
    bubble.alive = True
    return bubble


def update_bubble(cain, bubble):
    if bubble.alive:
        offset = Vec3(
            1.5 * random.uniform(0.8, 1.2),
            1.2,
            0
        )
        bubble.position = lerp(bubble.position, cain.position + offset, 2 * time.dt)


def start_bubble_autonomy(cain, bubble):
    def loop():
        while True:
            time.sleep(random.uniform(8, 14))
            if bubble.alive and random.random() < 0.15:
                speak_bubble("I'm gonna go do Bubble things!")
                bubble.visible = False
                bubble.alive = False

                def return_later():
                    time.sleep(random.uniform(15, 35))
                    bubble.visible = True
                    bubble.alive = True
                    speak_bubble("I'm baaaack!")

                threading.Thread(target=return_later, daemon=True).start()

    threading.Thread(target=loop, daemon=True).start()


def hide_bubble_temporarily(bubble):
    if bubble.alive:
        speak_bubble("Aaaaah! I'm gone!")
        bubble.visible = False
        bubble.alive = False

        def respawn():
            time.sleep(random.uniform(20, 40))
            bubble.visible = True
            bubble.alive = True
            speak_bubble("I'm baaaack!")

        threading.Thread(target=respawn, daemon=True).start()
