import time
import codigo_ia
import codigo_voz
from voz_a_texto import ReconocedorVoz

RUTA_MODELO = "resources/vosk-model-small-es-0.42"

def ejecutar_sistema():
    print("\n--- 🌀 SISTEMA ESPIRAL INICIADO (MODO OFFLINE) ---\n")

    try:
        ia_local = codigo_ia.ChatLocal()
        voz_entrada = ReconocedorVoz(RUTA_MODELO)
    except Exception as e:
        print("❌ Error iniciando componentes:", e)
        return

    # Saludo inicial
    voz_entrada.pausar() 
    codigo_voz.hablar("Sistema en línea")
    time.sleep(0.3) # Pausita de seguridad inicial
    voz_entrada.reanudar()
    print("🎤 Micrófono abierto. Esperando órdenes...")

    try:
        while True:
            user_input = voz_entrada.escuchar()

            if not user_input:
                continue

            print(f"\n👤 Tú: {user_input}")

            if user_input.lower() in ["salir", "exit", "adiós", "detener sistema"]:
                voz_entrada.pausar()
                codigo_voz.hablar("Cerrando sistema, hasta luego.")
                break

            print("⏳ Procesando con IA Local...")
            respuesta_ia = ia_local.obtener_respuesta(user_input)

            if not respuesta_ia:
                continue

            print(f"🌀 Espiral: {respuesta_ia}")

            # Bloqueo para evitar auto-escucha
            voz_entrada.pausar()

            # Hablar (espera a que termine el sonido)
            codigo_voz.hablar(respuesta_ia)

            # --- LA PAUSITA MILIMÉTRICA ---
            # Esperamos 300ms para que el eco ambiental se disipe totalmente
            time.sleep(0.3) 

            # Limpiar y reanudar
            voz_entrada.reanudar()
            print("🎤 Escuchando...")

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