import json
import os
import pyaudio
from vosk import Model, KaldiRecognizer

class ReconocedorVoz:
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
        self.activo = True

    def pausar(self):
        """Desactiva el procesamiento lógico del audio"""
        self.activo = False
        # Limpia lo que Vosk lleva acumulado para que no se trabe
        self.rec.Reset()

    def reanudar(self):
        """Limpia el eco residual y vuelve a escuchar"""
        # Primero tiramos a la basura cualquier ruido que haya entrado al cable
        try:
            while self.stream.get_read_available() > 0:
                self.stream.read(self.stream.get_read_available(), exception_on_overflow=False)
        except:
            pass
        
        # Reseteamos el reconocedor para empezar frase nueva
        self.rec.Reset()
        self.activo = True

    def escuchar(self):
        """Lee el audio solo si el sistema está activo"""
        if not self.activo:
            return None

        try:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.rec.AcceptWaveform(data):
                resultado = json.loads(self.rec.Result())
                texto = resultado.get("text", "").lower()
                return texto if texto.strip() else None
        except Exception as e:
            print(f"Error leyendo micro: {e}")
            
        return None

    def cerrar(self):
        """Cierra los recursos correctamente"""
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.mic.terminate()
        except:
            pass