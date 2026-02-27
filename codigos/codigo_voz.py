import os
import sounddevice as sd
import numpy as np
import queue
import time
from piper import PiperVoice

# --- CONFIGURACIÓN ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ruta exacta de el archivo
VOICE_PATH = r"C:\Users\Admin\Documents\Espiral\Espiral\resources\tts\es_MX-claude-high.onnx"

voice = PiperVoice.load(VOICE_PATH)
SAMPLE_RATE = voice.config.sample_rate

audio_queue = queue.Queue(maxsize=1000)

# --- GENERADOR DE TONO DE MANTENIMIENTO ---
def generar_tono_mantenimiento(frames):
    """Genera un tono de 20Hz casi inaudible para mantener el hardware activo."""
    t = np.arange(frames) / SAMPLE_RATE
    # 20Hz es el límite humano, el volumen es 0.01 (muy bajo pero existente para el DAC)
    onda = 0.01 * np.sin(2 * np.pi * 20 * t)
    # Convertimos a int16 para el stream
    return (onda * 32767).astype(np.int16)

def callback(outdata, frames, time, status):
    """Callback que inyecta el tono de mantenimiento si no hay voz."""
    try:
        data = audio_queue.get_nowait()
        if len(data) < frames:
            # Si el bloque de voz es corto, rellenamos con el tono de mantenimiento
            res = generar_tono_mantenimiento(frames)
            res[:len(data)] = data
            outdata[:, 0] = res
        else:
            outdata[:, 0] = data[:frames]
    except queue.Empty:
        # SI NO HAY VOZ: Reproduce el tono de 20Hz constantemente
        outdata[:, 0] = generar_tono_mantenimiento(frames)

# Stream con latencia 'low' para respuesta inmediata
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
    # Vaciamos la cola para que la nueva frase sea lo primero en sonar
    while not audio_queue.empty():
        try:
            audio_queue.get_nowait()
        except queue.Empty:
            break

   # print(f"🗣️ VoxControl dice: {texto}")
    
    try:
        # Síntesis de Piper
        for chunk in voice.synthesize(texto):
            audio_data = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
            
            # Mandamos la voz en bloques
            for i in range(0, len(audio_data), 512):
                block = audio_data[i:i+512]
                if len(block) < 512:
                    # Rellenamos el final con el tono de mantenimiento para no cortar
                    pad = generar_tono_mantenimiento(512)
                    pad[:len(block)] = block
                    block = pad
                audio_queue.put(block)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        # Mensaje inicial
        hablar("Modo activo")
        
        while True:
            t = input("\nEscribe algo: ")
            if t.lower() in ['salir', 's']: break
            hablar(t)
            
    except KeyboardInterrupt:
        stream.stop()
        print("\nCerrando sistema...")