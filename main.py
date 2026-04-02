from ursina import *
import threading

from ai.cain_ai import ai_loop
from characters.caine import create_caine, update_caine, start_caine_autonomy
from characters.bubble import create_bubble, update_bubble, start_bubble_autonomy
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

cain = create_caine()
bubble = create_bubble(cain)

start_caine_autonomy(cain)
start_bubble_autonomy(cain, bubble)

threading.Thread(target=ai_loop, args=(cain, bubble), daemon=True).start()

def update():
    update_caine(cain)
    update_bubble(cain, bubble)

app.run()
