import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Cargar variables de entorno
load_dotenv()
TOKEN_HF = os.getenv("HF_TOKEN")

if not TOKEN_HF:
    raise ValueError("No se encontró TOKEN_HF en el archivo .env")

# Cliente IA
client_ia = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=TOKEN_HF,
    timeout=30  # evita bloqueos infinitos
)

def obtener_respuesta(texto: str) -> str:
    """
    Envía texto al modelo y devuelve la respuesta.
    Maneja errores para que el sistema no se congele.
    """
    try:
        print("⏳ Llamando IA...")

        response = client_ia.chat_completion(
            messages=[
                {"role": "system", "content": "Eres un asistente inteligente y conciso."},
                {"role": "user", "content": texto}
            ],
            max_tokens=200,
            temperature=0.7
        )

        print("✅ Respuesta recibida")

        # Protección por si cambia la estructura
        if hasattr(response, "choices") and response.choices:
            return response.choices[0].message.content.strip()
        else:
            print("⚠️ Formato inesperado:", response)
            return "No pude procesar la respuesta correctamente."

    except Exception as e:
        print("❌ Error IA:", e)
        return "Hubo un error al procesar tu solicitud."


# Solo para prueba directa (no afecta tu main)
def chat():
    print("--- IA SISTEMA ---")
    while True:
        user_input = input("Tú: ")

        if user_input.lower() in ["salir", "exit"]:
            break

        respuesta = obtener_respuesta(user_input)
        print("IA:", respuesta)


if __name__ == "__main__":
    chat()