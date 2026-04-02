import pyttsx3
from queue import Queue
import threading

speech_queue = Queue()

engine_test = pyttsx3.init()
voices = engine_test.getProperty("voices")
cain_voice = voices[0].id
bubble_voice = voices[-1].id
del engine_test

def worker():
    while True:
        speaker, text = speech_queue.get()
        if text:
            engine = pyttsx3.init()

            # Force output to default audio device (headphones)
            try:
                engine.setProperty('outputDevice', 'Headphones')
            except:
                pass

            engine.setProperty("rate", 185)

            if speaker == "cain":
                engine.setProperty("voice", cain_voice)
                print(f"Cain: {text}")
            else:
                engine.setProperty("voice", bubble_voice)
                print(f"Bubble: {text}")

            engine.say(text)
            engine.runAndWait()
            engine.stop()

        speech_queue.task_done()

threading.Thread(target=worker, daemon=True).start()

def speak_cain(text):
    if text:
        speech_queue.put(("cain", text))

def speak_bubble(text):
    if text:
        speech_queue.put(("bubble", text))
