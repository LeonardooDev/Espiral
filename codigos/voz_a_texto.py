import json
import os
import pyaudio
from vosk import Model, KaldiRecognizer


class ReconocedorVoz:

    def pausar(self):
     self.stream.stop_stream()

    def reanudar(self):
     self.stream.start_stream()

    def __init__(self, ruta_modelo):
        if not os.path.exists(ruta_modelo):
            raise Exception(f"No se encontró el modelo en: {ruta_modelo}")

        self.model = Model(ruta_modelo)
        self.rec = KaldiRecognizer(self.model, 16000)

        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )

        self.stream.start_stream()

    def escuchar(self):
        data = self.stream.read(4000, exception_on_overflow=False)

        if self.rec.AcceptWaveform(data):
            resultado = json.loads(self.rec.Result())
            texto = resultado.get("text", "").lower()
            return texto if texto.strip() else None

        return None

    def cerrar(self):
        self.stream.stop_stream()
        self.stream.close()
        self.mic.terminate()