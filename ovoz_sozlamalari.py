import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
import pyttsx3
import datetime
import os

# --- Sozlamalar ---
MODEL_PATH = "path/to/vosk-model-small-uz-0.22"  # O'zbekcha Vosk modeli yo'li
SAMPLE_RATE = 16000
SILENCE_LIMIT = 20  # nechta bo'sh blokdan keyin gap tugadi (taxminan 2-3 soniya)

# --- TTS sozlash ---
engine = pyttsx3.init()
engine.setProperty('rate', 165)
engine.setProperty('volume', 1.0)

def speak(text):
    print("Bot:", text)
    engine.say(text)
    engine.runAndWait()

# --- Modelni yuklash ---
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("MODEL_PATH noto‘g‘ri! Model papkasini to‘g‘ri kiriting.")

print("Model yuklanmoqda...")
model = Model(MODEL_PATH)

# --- Audio navbat ---
audio_q = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print("Status:", status)
    audio_q.put(bytes(indata))

# --- Tinglash funksiyasi ---
def listen_once():
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    collected_text = ""
    silence_count = 0

    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        print("Gapiring...")

        while True:
            data = audio_q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                collected_text = result.get("text", "")
                break
            else:
                partial = json.loads(rec.PartialResult()).get("partial", "")
                if partial == "":
                    silence_count += 1
                else:
                    silence_count = 0

                if silence_count > SILENCE_LIMIT:
                    # Gap tugadi
                    final_result = json.loads(rec.FinalResult())
                    collected_text = final_result.get("text", "")
                    break

    return collected_text.strip()

# --- Javob tahlili ---
def analyze(text):
    t = text.lower()
    if "salom" in t:
        return "Va alaykum assalom!"
    elif "yaxshi" in t:
        return "Xursand bo'ldim."
    elif "soat" in t:
        now = datetime.datetime.now()
        return f"Hozir soat {now.strftime('%H:%M')}"
    elif "xayr" in t or "to'xta" in t:
        return "__EXIT__"
    else:
        return "Kechirasiz, buni tushunmadim."

# --- Asosiy sikl ---
def main():
    speak("Salom! Gapiring, men tinglayman.")
    while True:
        heard = listen_once()
        if not heard:
            speak("Tushunmadim.")
            continue
        print("Siz dedingiz:", heard)
        reply = analyze(heard)
        if reply == "__EXIT__":
            speak("Xayr!")
            break
        speak(reply)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDastur to'xtatildi.")
