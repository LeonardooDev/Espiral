import time
import codigo_ia
import codigo_voz
from voz_a_texto import ReconocedorVoz

RUTA_MODELO = "resources/vosk-model-small-es-0.42"


def ejecutar_sistema():
    print("\n--- 🌀 SISTEMA ESPIRAL INICIADO ---\n")

    try:
        # 🎤 Inicializar reconocimiento de voz
        voz_entrada = ReconocedorVoz(RUTA_MODELO)

    except Exception as e:
        print("❌ Error iniciando reconocimiento:", e)
        return

    # 🔊 Mensaje inicial
    codigo_voz.hablar("Sistema en línea")
    time.sleep(0.5)

    try:
        while True:

            # 🎤 Escuchar usuario
            user_input = voz_entrada.escuchar()

            if not user_input:
                continue

            print(f"\n👤 Tú: {user_input}")

            if user_input.lower() in ["salir", "exit", "s"]:
                codigo_voz.hablar("Cerrando sistema")
                break

            # 🤖 Llamar IA
            print("⏳ Procesando con IA...")
            respuesta_ia = codigo_ia.obtener_respuesta(user_input)

            if not respuesta_ia:
                print("⚠️ Respuesta vacía de IA")
                continue

            print(f"🌀 Espiral: {respuesta_ia}")

            # 🔊 Convertir respuesta a voz
            print("🔊 Enviando a síntesis...")

            # 🛑 Pausar micrófono
            voz_entrada.pausar()

            # 🔊 Hablar
            codigo_voz.hablar(respuesta_ia)

            # Esperar a que termine de hablar
            time.sleep(len(respuesta_ia) * 0.06)

            # 🎤 Reanudar micrófono
            voz_entrada.reanudar()

    except KeyboardInterrupt:
        print("\n🛑 Interrupción manual.")

    except Exception as e:
        print("❌ Error general del sistema:", e)

    finally:
        try:
            voz_entrada.cerrar()
        except Exception:
            pass

        print("\n✅ Sistema cerrado correctamente.")


if __name__ == "__main__":
    ejecutar_sistema()