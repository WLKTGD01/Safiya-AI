# import sounddevice as sd
# import queue
# import json
# import os
# import webbrowser
# from vosk import Model, KaldiRecognizer
#
# # ---- SOZLAMALAR ----
# MODEL_PATH = "path/to/vosk-model-small-uz-0.22"  # vosk modeli joylashgan papka
# SAMPLE_RATE = 16000
# q = queue.Queue()
#
# # Modelni yuklash
# if not os.path.exists(MODEL_PATH):
#     print("Model topilmadi! Iltimos, vosk o'zbek modelini yuklab 'model' papkasiga joylang.")
#     exit()
#
# model = Model(MODEL_PATH)
# recognizer = KaldiRecognizer(model, SAMPLE_RATE)
#
# # Ovoz olish callback
# def callback(indata, frames, time, status):
#     if status:
#         print(status)
#     q.put(bytes(indata))
#
# # Buyruqlarni bajarish
# def process_command(command):
#     if "pycharm" in command:
#         print("▶ Pycharm ishga tushyapti...")
#         os.startfile(r"C:\Program Files\JetBrains\PyCharm Community Edition 2023.2.5\bin\pycharm64.exe")
#
#     elif "google" in command:
#         print("▶ Google ochyapti...")
#         webbrowser.open("https://www.google.com")
#
#     elif "qidir" in command:
#         so_z = command.replace("qidir", "").strip()
#         if so_z:
#             print(f"▶ Google’da qidirilmoqda: {so_z}")
#             webbrowser.open(f"https://www.google.com/search?q={so_z}")
#         else:
#             print("❗ Qidirish so‘zi topilmadi.")
#
#     elif "word" in command:
#         print("▶ Microsoft Word ishga tushyapti...")
#         os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")
#
#     elif "stop" in command or "to'xta" in command:
#         print("❌ Dastur to‘xtadi.")
#         exit()
#
#     else:
#         print("❓ Buyruq topilmadi.")
#
# # Asosiy loop
# with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
#                        channels=1, callback=callback):
#     print("🎤 Gapiring... ('stop' yoki 'to‘xta' desangiz, dastur tugaydi)")
#     while True:
#         data = q.get()
#         if recognizer.AcceptWaveform(data):
#             result = recognizer.Result()
#             text = json.loads(result)["text"]
#             if text.strip():
#                 print("Siz dedingiz:", text)
#                 process_command(text)
import sounddevice as sd
import queue
import json
import os
import webbrowser
import pyttsx3
from vosk import Model, KaldiRecognizer

# ===== Jarvis Assistant =====
class JarvisAssistant:
    def __init__(self, model_path="path/to/vosk-model-small-uz-0.22", sample_rate=16000):
        self.model_path = model_path
        self.sample_rate = sample_rate
        self.q = queue.Queue()

        if not os.path.exists(model_path):
            raise FileNotFoundError("❗ Vosk modeli topilmadi. Iltimos, 'model' papkasiga yuklab qo'ying.")

        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, sample_rate)

        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)

    def speak(self, text):
        print("Jarvis:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(bytes(indata))

    def listen(self):
        with sd.RawInputStream(samplerate=self.sample_rate, blocksize=8000,
                               dtype="int16", channels=1, callback=self._callback):
            print("🎤 Gapiring...")
            while True:
                data = self.q.get()
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    text = json.loads(result)["text"]
                    if text.strip():
                        print("Siz dedingiz:", text)
                        return text.lower()

    def run(self):
        self.speak("Assalomu alaykum! Men Jarvisman. Buyruq bering.")
        while True:
            command = self.listen()

            if "pycharm" in command:
                self.speak("Pycharm ishga tushmoqda")
                os.startfile(r"C:\Program Files\JetBrains\PyCharm Community Edition 2023.2.5\bin\pycharm64.exe")

            elif "word" in command:
                self.speak("Microsoft Word ochilmoqda")
                os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")

            elif "paint" in command:
                self.speak("Paint ishga tushmoqda")
                os.startfile("mspaint.exe")

            elif "kalkulyator" in command or "calculator" in command:
                self.speak("Kalkulyator ochilmoqda")
                os.startfile("calc.exe")

            elif "google" in command and "qidir" not in command:
                self.speak("Google ochilmoqda")
                webbrowser.open("https://www.google.com")

            elif "qidir" in command:
                query = command.replace("qidir", "").strip()
                if query:
                    self.speak(f"Google’da qidirmoqdaman: {query}")
                    webbrowser.open(f"https://www.google.com/search?q={query}")
                else:
                    self.speak("Nimani qidiray?")

            elif "to'xta" in command or "stop" in command:
                self.speak("Xayr, dastur tugadi.")
                break

            else:
                self.speak("Bu buyruqni tushunmadim.")


if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run()
