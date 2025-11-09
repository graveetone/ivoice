import json
import wave
from vosk import Model, KaldiRecognizer

def get_text_from_audio_file(audio_file_path: str, vosk_model_path: str):
    model = Model(vosk_model_path)
    wf = wave.open(audio_file_path, "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
        raise ValueError("Аудіо повинно бути у форматі WAV, 16kHz, mono.")

    rec = KaldiRecognizer(model, wf.getframerate())
    text_result = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text_result += " " + result.get("text", "")

    result = json.loads(rec.FinalResult())
    text_result += " " + result.get("text", "")

    return text_result.strip()
