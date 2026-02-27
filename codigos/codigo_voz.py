import os
import sounddevice as sd
import numpy as np
import queue
import time
import pyttsx3
from piper import PiperVoice

engine = pyttsx3.init()

# --- CONFIGURACIÓN ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VOICE_PATH = r"C:\Users\Admin\Documents\Espiral\resources\tts\es_MX-claude-high.onnx"

voice = PiperVoice.load(VOICE_PATH)
SAMPLE_RATE = voice.config.sample_rate

audio_queue = queue.Queue(maxsize=1000)

def generar_tono_mantenimiento(frames):
    """Genera un tono casi inaudible para mantener el hardware activo."""
    t = np.arange(frames) / SAMPLE_RATE
    onda = 0.01 * np.sin(2 * np.pi * 20 * t)
    return (onda * 32767).astype(np.int16)

def callback(outdata, frames, time, status):
    try:
        data = audio_queue.get_nowait()
        if len(data) < frames:
            res = generar_tono_mantenimiento(frames)
            res[:len(data)] = data
            outdata[:, 0] = res
        else:
            outdata[:, 0] = data[:frames]
    except queue.Empty:
        outdata[:, 0] = generar_tono_mantenimiento(frames)

stream = sd.OutputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype='int16',
    callback=callback,
    blocksize=512,
    latency='low'
)
stream.start()

def hablar(texto):
    # 1. Limpiar rastro de pyttsx3 (si se usa)
    # engine.say(texto) # Comenta esto si solo usas Piper para evitar doble voz
    # engine.runAndWait()

    # 2. Vaciamos la cola vieja por seguridad
    while not audio_queue.empty():
        try:
            audio_queue.get_nowait()
        except queue.Empty:
            break

    try:
        # 3. Síntesis de Piper y llenado de cola
        for chunk in voice.synthesize(texto):
            audio_data = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
            
            for i in range(0, len(audio_data), 512):
                block = audio_data[i:i+512]
                if len(block) < 512:
                    pad = generar_tono_mantenimiento(512)
                    pad[:len(block)] = block
                    block = pad
                audio_queue.put(block)

        # --- EL TRUCO PARA EL MICRO ---
        # 4. Esperar a que la cola se vacíe REALMENTE en los altavoces
        while not audio_queue.empty():
            time.sleep(0.01) # Pausa mínima mientras el callback consume la cola
        
        # 5. Pequeño margen extra para que el eco desaparezca del aire
        time.sleep(0.2) 

    except Exception as e:
        print(f"❌ Error en síntesis: {e}")

if __name__ == "__main__":
    try:
        hablar("Modo activo")
        while True:
            t = input("\nEscribe algo: ")
            if t.lower() in ['salir', 's']: break
            hablar(t)
            print("Terminé de hablar.") # Verás que esto sale justo cuando el audio acaba
    except KeyboardInterrupt:
        stream.stop()