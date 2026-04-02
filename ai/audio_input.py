import sounddevice as sd
import whisper

print("Loading Whisper model...")
model = whisper.load_model("base")
print("Whisper loaded successfully.")

SAMPLE_RATE = 16000
DURATION = 3

def record_once():
    print("🎤 record_once() CALLED")

    try:
        print("🎤 Starting sd.rec()...")
        audio = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocking=True
        )
        sd.wait()
        print("🎤 Recording complete.")
        return audio.flatten()

    except Exception as e:
        print("❌ Microphone error:", e)
        return None


def transcribe(audio):
    if audio is None:
        print("❌ No audio to transcribe.")
        return ""

    print("📝 Transcribing...")
    try:
        result = model.transcribe(audio, fp16=False)
        print("📝 Transcription:", result["text"])
        return result["text"].strip()
    except Exception as e:
        print("❌ Whisper error:", e)
        return ""
