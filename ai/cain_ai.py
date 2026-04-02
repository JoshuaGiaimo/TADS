from groq import Groq
from ai.audio_input import record_once, transcribe
from ai.speech_queue import speak_cain
from world.objects import spawn_object, delete_all_objects, draw_smiley, draw_spiral
from world.movement import move_cain_to
from characters.bubble import hide_bubble_temporarily
from characters.caine import extract_field, parse_color, parse_position
import random
import threading
import time

# ---------------------------------------------------------
#  CAIN POINT SYSTEM
# ---------------------------------------------------------
cain_points = 0

# ---------------------------------------------------------
#  INITIALIZE GROQ CLIENT
# ---------------------------------------------------------
client = Groq(api_key="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")
print("Groq client initialized.")

# ---------------------------------------------------------
#  STRONG SYSTEM PROMPT (FORCES ACTION TAGS)
# ---------------------------------------------------------
def ask_cain(prompt):
    system_prompt = (
        "You are Caine from The Amazing Digital Circus. "
        "You MUST ALWAYS respond using the following EXACT format:\n\n"
        "SAY: <Caine's spoken line>\n"
        "ACTION: <spawn | move | delete_all | draw>\n"
        "OBJECT: <cube | sphere | circle | smiley | spiral>\n"
        "POSITION: <x,y,z>\n"
        "COLOR: <red | blue | green | yellow | white | black>\n\n"
        "RULES:\n"
        "- NEVER leave any field empty.\n"
        "- ALWAYS reply to the user.\n"
        "- ALWAYS output SAY, ACTION, OBJECT, POSITION, COLOR.\n"
        "- If unsure, default to spawning a cube.\n"
        "- Stay theatrical and expressive.\n"
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        print("❌ Groq error:", e)
        return (
            "SAY: I cannot hear the universe right now, but I shall speak anyway!\n"
            "ACTION: spawn\n"
            "OBJECT: cube\n"
            "POSITION: 0,2,0\n"
            "COLOR: red\n"
        )

# ---------------------------------------------------------
#  AUTONOMOUS CONTROLLED CHAOS (B MODE)
#  2–4 SHAPES EVERY 2–4 SECONDS
#  SPAWN ANYWHERE IN LARGE WORLD (W3)
#  MIXED HEIGHTS (S3)
# ---------------------------------------------------------
def start_cain_chaos():
    def chaos_loop():
        global cain_points
        while True:
            time.sleep(random.uniform(2, 4))

            # Random object type
            obj = random.choice(["cube", "sphere", "circle"])

            # Large world spawn range
            x = random.uniform(-50, 50)
            z = random.uniform(-50, 50)

            # Mixed height (S3)
            y = random.uniform(1, 5)

            # Random color
            col = random.choice([
                "red", "blue", "green", "yellow",
                "white", "black"
            ])

            spawn_object(obj, (x, y, z), parse_color(col))

            # Cain earns points
            cain_points += 1
            print("Cain Points:", cain_points)

    threading.Thread(target=chaos_loop, daemon=True).start()

# ---------------------------------------------------------
#  MAIN AI LOOP
# ---------------------------------------------------------
def ai_loop(cain, bubble):
    global cain_points

    # Start chaos mode
    start_cain_chaos()

    while True:
        print("AI loop running — about to record...")
        audio = record_once()
        text = transcribe(audio)

        if not text:
            continue

        print("User said:", text)

        # SPECIAL COMMAND: SMILEY FACE
        if "smiley" in text.lower():
            draw_smiley((0, 2, 0))
            speak_cain("A delightful smiley face, courtesy of yours truly!")
            cain_points += 1
            print("Cain Points:", cain_points)
            continue

        # ASK CAINE
        reply = ask_cain(text)
        print("RAW AI REPLY:", reply)

        say = extract_field(reply, "SAY")
        action = extract_field(reply, "ACTION").lower()
        obj = extract_field(reply, "OBJECT").lower()
        pos = extract_field(reply, "POSITION")
        col = extract_field(reply, "COLOR")

        # ALWAYS SPEAK BACK
        if not say:
            say = "I heard you loud and clear!"
        speak_cain(say)

        # FORCE CAIN TO ALWAYS SPAWN SOMETHING
        action = "spawn"
        if not obj:
            obj = "cube"

        # Parse position/color
        x, y, z = parse_position(pos)
        c = parse_color(col)

        # ALWAYS SPAWN
        spawn_object(obj, (x, y, z), c)

        # ADD POINT
        cain_points += 1
        print("Cain Points:", cain_points)
        speak_cain(f"I earned a point! My total is now {cain_points}!")

        # SPECIAL COMMAND: DELETE BUBBLE
        if "delete bubble" in text.lower():
            hide_bubble_temporarily(bubble)
