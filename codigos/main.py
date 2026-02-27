import codigo_ia
import codigo_voz

def ejecutar_sistema():
    print("--- 🌀 SISTEMA ESPIRAL INICIADO ---")
    # Mensaje inicial de bienvenida
    codigo_voz.hablar("Sistema en línea")

    while True:
        try:
            # 1. Capturamos la entrada del usuario
            user_input = input("\n👤 Tú: ")
            
            if user_input.lower() in ["salir", "exit", "s"]:
                codigo_voz.hablar("Cerrando sistema")
                break

            # 2. Llamamos a la lógica de la IA (del archivo ia.py)
            # Nota: Usamos la función de chat simplificada
            respuesta_ia = codigo_ia.client_ia.chat_completion(
                messages=[{"role": "user", "content": user_input}],
                max_tokens=300
            ).choices[0].message.content
            
            print(f"🌀 Espiral: {respuesta_ia}")

            # 3. Pasamos el texto de la IA al motor de voz (del archivo codigo_voz.py)
            codigo_voz.hablar(respuesta_ia)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error en el flujo principal: {e}")

if __name__ == "__main__":
    try:
        ejecutar_sistema()
    finally:
        # Cerramos el stream de audio al salir
        codigo_voz.stream.stop()
        codigo_voz.stream.close()
        print("\nSaliendo...")